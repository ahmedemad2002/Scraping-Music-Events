import scrapy
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Lawrence.items import EventItem
import re
import json

class EventbriteSpider(scrapy.Spider):
    name = "eventbrite"

    custom_settings = {
        "LOG_LEVEL": "INFO"
    }

    def __init__(self, s_date=None, e_date=None):
        if s_date is None:
            s_date = datetime.now().strftime("%Y-%m-%d")
        if e_date is None:
            e_date = (datetime.strptime(s_date, '%Y-%m-%d') + relativedelta(months=1)).strftime("%Y-%m-%d")
        super(EventbriteSpider, self).__init__()
        self.s_date = s_date
        self.e_date = e_date

    def start_requests(self):
        yield scrapy.Request(f"https://www.eventbrite.com/d/wa--seattle/music--events/?page=1&start_date={self.s_date}&end_date={self.e_date}", callback=self.n_of_pages)

    def n_of_pages(self, response):
        pag_dict = response.css('script[type="text/javascript"]::text').getall()[-1].split('"pagination":')[-1].split('}')[0] + "}"
        pag_dict = json.loads(pag_dict)
        n_pages = pag_dict['page_count']
        self.parse_urls(response)
        for i in range(2, n_pages+1):
            yield scrapy.Request(url=f"https://www.eventbrite.com/d/wa--seattle/music--events/?page={i}&start_date={self.s_date}&end_date={self.e_date}", callback=self.parse_urls)
        
    def parse_urls(self, response):
        urls = response.css('a.event-card-link::attr(href)').getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        server_data = response.text[response.text.index("window.__SERVER_DATA__ = "):]
        server_data = server_data[:server_data.index("</script>")]
        server_data = server_data.strip().replace(';', '')
        server_data = server_data.replace('window.__SERVER_DATA__ = ', '')
        try:
            server_data_dict = json.loads(server_data[server_data.index('{'): server_data.rfind('}')])
            price = server_data_dict['components']['conversionBar']['statusToDisplay']
        except Exception as e:
            print(f"error {e} in the {response.url}, and this is server_data::: {server_data}")
            price = None
        
        if " – " in price:
            lp, hp = price.split(' – ')
        else:
            price= price.replace('Free', '$0')
            lp = hp = price
        
        full_address = response.css('meta[name="twitter:data1"]::attr(value)').get()
        address, city, state_zip_code = full_address.split(', ')[:3]
        try:
            state, zip_code = state_zip_code.split(' ')[:2]
        except:
            state = state_zip_code
            zip_code = None
        dt = response.css('meta[property="event:start_time"]::attr(content)').get()
        o = EventItem()
        o['event_title'] = response.css('h1.event-title::text').get()
        o['venue_title'] = response.css('p.location-info__address-text::text').get()
        o['address'] = address
        o['zip_code'] = zip_code
        o['city'] = city
        o['state'] = state
        o['phone_number'] = None
        o['date'], o['time'] = dt.split('T')
        o['time'] = ':'.join(o['time'].split(':')[:2])
        o['lowest_price'], o['highest_price'] = lp, hp
        o['source_url'] = response.url
        yield o