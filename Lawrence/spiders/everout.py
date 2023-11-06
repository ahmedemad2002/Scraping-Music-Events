import scrapy
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import json
from Lawrence.items import EventItem


class EveroutSpider(scrapy.Spider):
    name = "everout"

    def __init__(self, s_date=None, e_date=None):
        if s_date is None:
            s_date = datetime.now().strftime("%Y-%m-%d")
        if e_date is None:
            (datetime.strptime(s_date, '%Y-%m-%d') + relativedelta(months=1)).strftime("%Y-%m-%d")
        super(EveroutSpider, self).__init__()
        self.s_date = s_date
        self.e_date = e_date

    def start_requests(self):
        yield scrapy.Request(
            url=f"https://everout.com/seattle/events/?page=1&category=live-music&start-date={self.s_date}&end-date={self.e_date}",
            callback=self.n_pages)

    def n_pages(self, response):
        n_pages = response.css('.pagination-description::text').get()
        if n_pages is None:
            n_pages = 1
        else:
            n_pages = n_pages.split(' ')
            n_pages = ' '.join(n_pages).strip().split(' ')[-1]
            n_pages = int(n_pages)
        for i in range(1, n_pages + 1):
            yield scrapy.Request(
                url=f"https://everout.com/seattle/events/?page={i}&category=live-music&start-date={self.s_date}&end-date={self.e_date}",
                callback=self.events_urls, dont_filter=True)

    def events_urls(self, response):
        urls = response.css('.event-list .row h2 a::attr(href)').getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_event, errback=self.errback_httpbin)

    def parse_event(self, response):
        price=''.join(response.css('.price::text').getall()).strip().split(' - ')
        lp = price[0].replace('$', '')
        hp=None
        if len(price)>1:
            hp=price[1].replace('$', '')
        if lp=="Free":
            lp= hp= float(0)
        try:
            lp= float(lp)
        except:
            lp=float(0)
        try:
            if hp is not None:
                hp= float(hp)
        except:
            hp=float(0)
        zipcode_pattern = re.compile(r'\d{5}')
        venue_location = ''.join(response.css('.location-info::text').getall()).strip()
        zipcode = re.search(zipcode_pattern, venue_location)
        zipcode = zipcode.group(0) if zipcode else None
        o = EventItem()
        o['event_title'] = response.css('h1.mb-0::text').get()
        o['venue_title'] = response.css('.location-info a::text').get()
        o['address'] = venue_location.split('\n')[0]
        o['zip_code'] = zipcode
        o['city'] = venue_location.split('\n')[1].split(', ')[0] if len(venue_location.split('\n'))>1 else None
        o['state'] = venue_location.split('\n')[1].split(', ')[1].split(' ')[0] if len(venue_location.split('\n'))>1 else None
        o['phone_number'] = None
        o['date'] = o['time'] = None #will be scraped later from the API request
        o['lowest_price'] = lp
        o['highest_price'] = hp
        o['source_url'] = response.url
        event_id = response.url.split('/')[-2].replace('e', '')
        yield scrapy.Request(url=f'https://everout.com/api/schedule-dates/?market=seattle&page_size=300&occurrence={event_id}', callback=self.parse_dates, meta={'object': o})

    def parse_dates(self, response):
        o = response.meta['object']
        res = json.loads(response.text)
        n_dates = res['count']
        for i in range(n_dates):
            event_time = res['results'][i]['schedule']['start_time']
            if event_time is not None:
                event_time = ':'.join(event_time.split(':')[:-1])
            event_datetime = {"Date": res['results'][i]['date'], "Time": event_time}
            if event_datetime['Date'] <= self.e_date:
                o['date'] = event_datetime['Date']
                o['time'] = event_datetime['Time']
                yield o
        

    # Error handling for request failures
    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))

        # In case you want to perform some actions on failure, you can add them here.
