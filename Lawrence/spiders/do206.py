import scrapy
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Lawrence.items import EventItem
import re

class Do206Spider(scrapy.Spider):
    name = "do206"
    BASE_URL = "https://do206.com"    
    headers={
        'Cookie': '_lc2_fpi=3ccf42027f98--01hdmrq38vxvbfra2rafy99rwc; _lc2_fpi_meta={%22w%22:1698282835227}; __li_idexc=1; _fbp=fb.1.1698282835952.1653543430; has_feed_alert=true; __qca=P0-1412446113-1698282837545; hubspotutk=5b58e659191bc7f10bf91eac6ab316f8; _li_ss=CngKBQgKELIWCgYI3QEQshYKBQgJELIWCgYI4QEQshYKBgiBARCyFgoGCKIBELIWCgkI_____wcQthYKBgiLARCyFgoGCKQBELIWCgYIswEQshYKBgiJARCyFgoGCKUBELIWCgYI0gEQshYKBQh-ELIWCgYIiAEQshY; _session_id=2ae9de42866e50265b7d7a5b54049280; _gid=GA1.2.1062985302.1698905023; i18next=en; page_view=%2Fevents%2Ftoday; _ga_B9RF859PFK=GS1.1.1698905019.9.1.1698905750.0.0.0; _li_dcdm_c=.do206.com; __li_idexc_meta={%22w%22:1698905751134%2C%22e%22:1699510551134}; _gat=1; _gat_t3=1; _ga_TFP440N6SQ=GS1.1.1698905019.5.1.1698905751.0.0.0; _ga=GA1.1.199830866.1698282836; scarab.visitor=%227A15A535D5722197%22; _li_ss_meta={%22w%22:1698905753615%2C%22e%22:1701497753615}; __hstc=73576333.5b58e659191bc7f10bf91eac6ab316f8.1698282842611.1698905044371.1698905753754.10; __hssrc=1; __hssc=73576333.1.1698905753754'
        
    }
    
    def __init__(self, s_date=None, e_date=None):
        if s_date is None:
            s_date = datetime.now().strftime("%Y-%m-%d")
        if e_date is None:
            e_date = (datetime.strptime(s_date, '%Y-%m-%d') + relativedelta(months=1)).strftime("%Y-%m-%d")
        super(Do206Spider, self).__init__()
        self.s_date = s_date
        self.e_date = e_date
    
    def start_requests(self):
        url = "https://do206.com/events/music/{}"
        # Convert the start and end dates to datetime objects
        start_date = datetime.strptime(self.s_date, '%Y-%m-%d')
        end_date = datetime.strptime(self.e_date, '%Y-%m-%d')
        current_date = start_date
        # Loop through the dates, including the end date
        while current_date <= end_date:
            curr_date = current_date.strftime('%Y/%m/%d')  # Print the current date
            current_date += timedelta(days=1)  # Increment the current date by one day
            yield scrapy.Request(url=url.format(curr_date), headers=self.headers, callback=self.parse_urls)
            
            
    def parse_urls(self, response):
        urls = response.css('a.ds-listing-event-title.url.summary::attr(href)').getall()
        for url in urls:
            yield scrapy.Request(url=self.BASE_URL+url, headers=self.headers, callback=self.parse)
        next_page = response.css('.ds-next-page::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(url=self.BASE_URL+next_page, headers=self.headers, callback=self.parse_urls)

    def parse(self, response):
        dt = response.css('meta[itemprop="startDate"]::attr(content)').get()
        price = response.css('h2.ds-ticket-info::text').get()
        try:
            prices = re.findall(r'\$(\d+)(?!\+)', price)
        except TypeError:
            prices = None
            print(f"Error in extracting the price from {price}")
            
        o = EventItem()
        o['event_title'] = response.css('h1 span.ds-event-title-text::text').get()
        o['venue_title'] = response.css('a h2 span::text').get()
        o['address'] = response.css('meta[itemprop="streetAddress"]::attr(content)').get()
        o['zip_code'] = response.css('meta[itemprop="postalCode"]::attr(content)').get()
        o['city'] = response.css('meta[itemprop="addressLocality"]::attr(content)').get()
        o['state'] = response.css('meta[itemprop="addressRegion"]::attr(content)').get()
        o['phone_number'] = None
        o['date'] = dt.split('T')[0]
        o['time'] = dt.split('T')[1].split('-')[0]
        # Initialize lowest_price and highest_price with None values
        o['lowest_price'] = None
        o['highest_price'] = None
        # Assign values if prices list is not None and has sufficient elements
        if prices:
            if len(prices) >= 1:
                o['lowest_price'] = prices[0]
            if len(prices) >= 2:
                o['highest_price'] = prices[1]
        o['source_url'] = response.url
        yield o