import scrapy
import json
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta
from Lawrence.items import EventItem

class SeatgeekSpider(scrapy.Spider):
    name = "seatgeek"
    download_delay = 75
    randomize_download_delay= False
    
    cookie_str = "sixpack_client_id=74596320-27f1-4998-989e-08c96bb01892; sg_l=en-US; sg_c=USD; sg_uuid=b3a92a77-1bbf-b1e4-95bd-eec44db1634b; sixpack_client_id=74596320-27f1-4998-989e-08c96bb01892; sg_session=d1dfe8b396bf758fd24c63fcc6193fa6; __ssid=2638bf4c3011fd9159bea27ca209c36; _gcl_au=1.1.2047420590.1698738187; _swb_consent_=eyJvcmdhbml6YXRpb25Db2RlIjoic2VhdGdlZWsiLCJwcm9wZXJ0eUNvZGUiOiJzZWF0Z2Vla19jb20iLCJlbnZpcm9ubWVudENvZGUiOiJwcm9kdWN0aW9uIiwiaWRlbnRpdGllcyI6eyJzZWF0Z2Vla19zaXhwYWNrX2lkX2Jhc2VkX2lkZW50aXR5IjoiNzQ1OTYzMjAtMjdmMS00OTk4LTk4OWUtMDhjOTZiYjAxODkyIiwic3diX3NlYXRnZWVrX2NvbSI6ImIzYTkyYTc3LTFiYmYtYjFlNC05NWJkLWVlYzQ0ZGIxNjM0YiJ9LCJqdXJpc2RpY3Rpb25Db2RlIjoiZGVmYXVsdCIsInB1cnBvc2VzIjp7ImFuYWx5dGljcyI6eyJhbGxvd2VkIjoidHJ1ZSIsImxlZ2FsQmFzaXNDb2RlIjoiZGlzY2xvc3VyZSJ9LCJlc3NlbnRpYWxfcHVycG9zZXMiOnsiYWxsb3dlZCI6InRydWUiLCJsZWdhbEJhc2lzQ29kZSI6ImRpc2Nsb3N1cmUifSwicGVyc29uYWxpc2F0aW9uIjp7ImFsbG93ZWQiOiJ0cnVlIiwibGVnYWxCYXNpc0NvZGUiOiJkaXNjbG9zdXJlIn0sInByb2R1Y3RfZW5oYW5jZW1lbnQiOnsiYWxsb3dlZCI6InRydWUiLCJsZWdhbEJhc2lzQ29kZSI6ImRpc2Nsb3N1cmUifX0sImNvbGxlY3RlZEF0IjoxNjk4NzM4MTg3fQ%3D%3D; _ketch_consent_v1_=eyJhbmFseXRpY3MiOnsic3RhdHVzIjoiZ3JhbnRlZCIsImNhbm9uaWNhbFB1cnBvc2VzIjpbImFuYWx5dGljcyJdfSwiZXNzZW50aWFsX3B1cnBvc2VzIjp7InN0YXR1cyI6ImdyYW50ZWQiLCJjYW5vbmljYWxQdXJwb3NlcyI6WyJlc3NlbnRpYWxfc2VydmljZXMiXX0sInBlcnNvbmFsaXNhdGlvbiI6eyJzdGF0dXMiOiJncmFudGVkIiwiY2Fub25pY2FsUHVycG9zZXMiOlsicGVyc29uYWxpemF0aW9uIl19LCJwcm9kdWN0X2VuaGFuY2VtZW50Ijp7InN0YXR1cyI6ImdyYW50ZWQiLCJjYW5vbmljYWxQdXJwb3NlcyI6WyJwcm9kX2VuaGFuY2VtZW50Il19fQ%3D%3D; _ga=GA1.2.494591684.1698738187; _uetvid=bf0b627073e511ee94184fd0e4873797; _fbp=fb.1.1698738188360.834134920; IR_PI=040e8f64-1bce-11ee-af34-3b90f22b7458%7C1698824588136; _ga_44M3TK17XS=GS1.1.1698743230.2.0.1698743230.60.0.0; datadome=tAgF5leGygyFgHhTb3e~BQLFkpkU8SACDH~uSq4VHlzOPBuv0MHpzcD3ICdS80z5RYxxuaR3vEL04Xj5TShxkU9CTtvDpGHLm1hrzp9090tU~m7aFNv6tjTUms7P2lgY"
    cookies = {x.split('=')[0]: x.split('=')[1] for x in  cookie_str.split(';')}
    
    def __init__(self, s_date=None, e_date=None):
        if s_date is None:
            s_date = datetime.now().strftime("%Y-%m-%d")
        if e_date is None:
            e_date = (datetime.strptime(s_date, '%Y-%m-%d') + relativedelta(months=1)).strftime("%Y-%m-%d")
        super(SeatgeekSpider, self).__init__()
        self.s_date = s_date
        self.e_date = e_date

    def start_requests(self):
        api_url = "https://seatgeek.com/api/events?page=1&listing_count.gte=1&lat=47.61&lon=-122.33&range=54mi&sort=datetime_local.asc&taxonomies.id=2000000&client_id=MTY2MnwxMzgzMzIwMTU4&per_page=50"
        
        yield scrapy.Request(url=api_url, cookies=self.cookies, callback=self.n_of_pages)

    def n_of_pages(self, response):
        res = json.loads(response.text)
        n_pages= math.ceil(res['meta']['total']/50)
        api_url = "https://seatgeek.com/api/events?page={}&listing_count.gte=1&lat=47.61&lon=-122.33&range=54mi&sort=datetime_local.asc&taxonomies.id=2000000&client_id=MTY2MnwxMzgzMzIwMTU4&per_page=50"
        for i in range(1, n_pages+1):
            yield scrapy.Request(url=api_url.format(i), cookies=self.cookies, callback=self.parse, meta={'pagenum': i}, dont_filter=True)
    def parse(self, response):
        res = json.loads(response.text)
        if response.meta['pagenum'] != res['meta']['page']:
            print(f"API sent page {res['meta']['page']} instead of page {response.meta['pagenum']}")
            yield scrapy.Request(response.url, cookies=self.cookies, callback=self.parse, meta=response.meta)
        else:
            events = res['events']
            for event in events:
                e = EventItem()
                e['event_title'] = event['title']
                e['venue_title'] = event['venue']['name']
                e['address'] = event['venue']['address']
                e['zip_code'] = event['venue']['postal_code']
                e['city'] = event['venue']['city']
                e['state'] = event['venue']['state']
                e['phone_number'] = None
                e['date'] = event['datetime_local'].split('T')[0]
                e['time'] = ':'.join(event['datetime_local'].split('T')[1].split(':')[:-1])
                e['lowest_price'] = event['stats']['lowest_price']
                e['highest_price'] = event['stats']['highest_price']
                e['source_url'] = event['url']
                if e['date'] <= self.e_date:
                    yield e
                