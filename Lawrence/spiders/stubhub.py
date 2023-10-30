import scrapy
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Lawrence.items import EventItem
import re
import json
from math import ceil



class StubhubSpider(scrapy.Spider):
    name = "stubhub"
    BASE_URL = "https://www.stubhub.com"
    
    def __init__(self, s_date=None, e_date=None):
        if s_date is None:
            s_date = datetime.now().strftime("%Y-%m-%d")
        if e_date is None:
            e_date = (datetime.strptime(s_date, '%Y-%m-%d') + relativedelta(months=1)).strftime("%Y-%m-%d")
        super(StubhubSpider, self).__init__()
        self.s_date = s_date
        self.e_date = e_date
    
    def start_requests(self):
        start_date = datetime.strptime(self.s_date, "%Y-%m-%d")
        s_timestamp = int(start_date.timestamp())
        end_date = datetime.strptime(self.e_date, "%Y-%m-%d")
        e_timestamp = int(end_date.timestamp())
        start, end = s_timestamp*1000, e_timestamp*1000
        yield scrapy.Request(url=f"https://www.stubhub.com/concert-tickets/category/1?method=getExploreEvents&from={start}&lat=NDcuNjA2&lon=LTEyMi4zMzM%3D&to={end}&page=0&tlcId=3", callback=self.n_of_pages)
    
    def n_of_pages(self, response):
        res = json.loads(response.text)
        n_pages = ceil(res['total']/12)
        for i in range(n_pages+1):
            yield scrapy.Request(url=response.url.replace('page=0', f'page={i}'), callback=self.parse_urls, dont_filter=True)
    
    def parse_urls(self, response):
        res= json.loads(response.text)
        events = res['events']
        for event in events:
            yield scrapy.Request(url=self.BASE_URL+event['url'], callback=self.parse, meta={'event_name': event['name'], 'venue_name': event['venueName']})
    
    def parse(self, response):
        s = response.css('#index-data::text').get().strip()
        sd = json.loads(s)
        venued = json.loads(response.css('script[type="application/ld+json"]::text').get().strip())
        location = venued['location']['address']
        o = EventItem()
        o['event_title'] = response.meta['event_name']
        o['venue_title'] = response.meta['venue_name']
        o['address'] = location['streetAddress']
        o['zip_code'] = location['postalCode']
        o['city'] = sd['venueCity']
        o['state'] = sd['venueStateProvinceName']
        o['phone_number'] = None
        o['date'] = venued['startDate'].split('T')[0]
        o['time'] = ':'.join(venued['startDate'].split('T')[1].split(':')[:2])
        o['lowest_price'] = sd['grid']['minPrice']
        o['highest_price'] = sd['grid']['maxPrice']
        o['source_url'] = response.url
        yield o
