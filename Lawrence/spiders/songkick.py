import scrapy
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

class SongkickSpider(scrapy.Spider):
    name = "songkick"
    BASE_URL = "https://www.songkick.com"

    def __init__(self, s_date=None, e_date=None):
        super(SongkickSpider, self).__init__()
        if s_date is None:
            s_date = datetime.now().strftime("%Y-%m-%d")
        if e_date is None:
            e_date = (datetime.strptime(s_date, '%Y-%m-%d') + relativedelta(months=1)).strftime("%Y-%m-%d")
        s_date = datetime.strptime(s_date, "%Y-%m-%d")
        e_date = datetime.strptime(e_date, "%Y-%m-%d")
        self.s_date = s_date.strftime('%m%%2F%d%%2F%Y')
        self.e_date = e_date.strftime('%m%%2F%d%%2F%Y')

    
    def API_Request(self, page_num, s_date, e_date):
        API_URL = f"https://www.songkick.com/metro-areas/2846-us-seattle?filters%5BmaxDate%5D={e_date}&filters%5BminDate%5D={s_date}&page={page_num}#metro-area-calendar"
        return API_URL
    
    def start_requests(self):
        yield scrapy.Request(url=self.API_Request(1, self.s_date, self.e_date), callback=self.N_of_pages)
        
    def N_of_pages(self, response):
        n_pages = int(response.css('div.pagination a::text').getall()[-2])
        for i in range(1, n_pages+1):
            yield scrapy.Request(url=self.API_Request(i, self.s_date, self.e_date), callback=self.events_urls, dont_filter=True)
    
    
    def events_urls(self, response):
        urls = response.css('a.event-link.chevron-wrapper::attr(href)').getall()
        for url in urls:
            yield scrapy.Request(url=self.BASE_URL+url, callback=self.parse)
    
    def parse(self, response):
        address = response.css('.venue-hcard span::text').getall()
        address = [a for a in address if not a.startswith('\n')]
        location = ' '.join(address)
        location = self.extract_address_data_v5(location)
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        date_string = response.css('.date-and-name p::text').get().split(' – ')[0]
        formatted_date = datetime.strptime(date_string, "%A %d %B %Y").strftime("%m/%d/%Y")

        try:
            price=response.css('.additional-details-container::text').get().split(':')[1].strip()
            try:
                lp, hp = price.split(' – ')
                lp, hp = lp.replace('US $', ''), hp.replace('US $', '')
            except:
                lp, hp = price.replace('US $', ''), None
        except:
            lp, hp = None, None
        try:
            opens = response.css('.additional-details-container p::text').get().split('Doors open: ')[1]
        except:
            opens = None
        o = {}
        o['event_title'] = ''.join(response.css('h1.h0 *::text').getall()).strip()
        o['venue_title'] = response.css('div.venue-info-details a.url::text').get()
        # o['Description'] = None
        o['address'] = location['address']
        o['zip_code'] = location['zipcode']
        o['city'] = location['city']
        o['state'] = location['state']
        o['phone_number'] = location['phone']
        o['date'] = formatted_date
        o['time'] = opens
        o['lowest_price'] = lp
        o['highest_price'] = hp
        o['source_url'] = response.url
        yield o

    def extract_address_data_v5(self, entry):
        zipcode_pattern = re.compile(r'\d{5}')
        city_state_pattern = re.compile(r'(\w+),\s*(WA),\s*US')
        phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        # Ensure entry is a string
        if not isinstance(entry, str):
            entry = str(entry)

        zipcode = re.search(zipcode_pattern, entry)
        city_state = re.search(city_state_pattern, entry)
        phone = re.search(phone_pattern, entry)

        # Remove the extracted parts to get the address
        address = entry
        for pattern in [zipcode_pattern, city_state_pattern, phone_pattern]:
            match = re.search(pattern, address)
            if match:
                address = address.replace(match.group(0), '').strip()

        zipcode = zipcode.group(0) if zipcode else None
        city = city_state.group(1) if city_state else None
        state = city_state.group(2) if city_state else None
        phone = phone.group(0) if phone else None
        return {"address": address, 'zipcode': zipcode, 'city': city, 'state': state, 'phone': phone}
        