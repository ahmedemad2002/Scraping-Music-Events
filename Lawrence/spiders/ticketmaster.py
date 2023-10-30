import scrapy
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from Lawrence.items import EventItem


class TicketmasterSpider(scrapy.Spider):
    name = "ticketmaster"

    def __init__(self, s_date=None, e_date=None):
        if s_date is None:
            s_date = datetime.now().strftime("%Y-%m-%d")
        if e_date is None:
            e_date = (datetime.strptime(s_date, '%Y-%m-%d') + relativedelta(months=1)).strftime("%Y-%m-%d")
        super(TicketmasterSpider, self).__init__()
        self.s_date = s_date
        self.e_date = e_date

    def API_Request(self, page_num, s_date, e_date, page_size=200):
        API_URL = f"https://www.ticketmaster.com/api/next/graphql?operationName=CategorySearch&variables=%7B%22locale%22%3A%22en-us%22%2C%22sort%22%3A%22date%2Casc%22%2C%22page%22%3A{page_num}%2C%22size%22%3A{page_size}%2C%22lineupImages%22%3Atrue%2C%22withSeoEvents%22%3Atrue%2C%22radius%22%3A%22100%22%2C%22geoHash%22%3A%22c23n%22%2C%22unit%22%3A%22miles%22%2C%22segmentId%22%3A%22KZFzniwnSyZfZ7v7nJ%22%2C%22localeStr%22%3A%22en-us%22%2C%22type%22%3A%22event%22%2C%22localStartEndDateTime%22%3A%22{s_date}T00%3A00%3A00%2C{e_date}T23%3A59%3A59%22%2C%22includeDateRange%22%3Atrue%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%225664b981ff921ec078e3df377fd4623faaa6cd0aa2178e8bdfcba9b41303848b%22%7D%7D"
        return API_URL

    def start_requests(self):
        url = self.API_Request(page_num=0, s_date=self.s_date, e_date=self.e_date)
        yield scrapy.Request(url=url, callback=self.N_of_pages)

    def N_of_pages(self, response):
        res = json.loads(response.text)
        n_pages = res['data']['products']['page']['totalPages']
        for i in range(n_pages):
            yield scrapy.Request(url=self.API_Request(page_num=i, s_date=self.s_date, e_date=self.e_date),
                                 callback=self.parse, dont_filter=True)

    def parse(self, response):
        res = json.loads(response.text)
        items = res['data']['products']['items']
        for item in items:
            address = item['venues'][0]
            price = item['priceRanges']
            if price is not None:
                price = price[0]['min']

            datetime_string = item['datesFormatted']['venueDateTime']
            # Parse the datetime string
            parsed_datetime = datetime.fromisoformat(datetime_string)
            # Format the date as "MM-DD-YYYY"
            formatted_date = parsed_datetime.strftime("%m-%d-%Y")
            # Format the time as "HH:MM"
            formatted_time = parsed_datetime.strftime("%H:%M")
            o = EventItem()
            o['event_title'] = item['name']
            o['venue_title'] = address['name']
            o['address'] = address['address']['line1']
            o['zip_code'] = address['postalCode']
            o['city'] = address['city']['name']
            o['state'] = address['state']['name']
            o['phone_number'] = None
            o['date'] = formatted_date
            o['time'] = formatted_time
            o['lowest_price'] = price
            o['highest_price'] = None
            o['source_url'] = item['eventUrlLink']
            yield o
