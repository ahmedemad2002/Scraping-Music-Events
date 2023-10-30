import scrapy
import json
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta
from Lawrence.items import EventItem

class SeatgeekSpider(scrapy.Spider):
    name = "seatgeek"
    download_delay = 65
    
    
    cookie_str = "sg_l=en-US; sg_c=USD; sixpack_client_id=af088c10-23c2-4db4-a5a7-89d464572708; sg_uuid=be7130ba-1306-48c4-1d2d-c44481188342; sixpack_client_id=af088c10-23c2-4db4-a5a7-89d464572708; sg_session=7855c56dabda524bdd29b3e21e878e41; SeatGeekEntrance=category=entrance%3Bdt=%3Bap=%3BadId=; __ssid=31f81c4bba3f580088d985f145aa7fa; _gcl_au=1.1.999870122.1698314108; IR_gbd=seatgeek.com; _fbp=fb.1.1698314108708.413543419; _ketch_consent_v1_=eyJhbmFseXRpY3MiOnsic3RhdHVzIjoiZ3JhbnRlZCIsImNhbm9uaWNhbFB1cnBvc2VzIjpbImFuYWx5dGljcyJdfSwiZXNzZW50aWFsX3B1cnBvc2VzIjp7InN0YXR1cyI6ImdyYW50ZWQiLCJjYW5vbmljYWxQdXJwb3NlcyI6WyJlc3NlbnRpYWxfc2VydmljZXMiXX0sInBlcnNvbmFsaXNhdGlvbiI6eyJzdGF0dXMiOiJncmFudGVkIiwiY2Fub25pY2FsUHVycG9zZXMiOlsicGVyc29uYWxpemF0aW9uIl19LCJwcm9kdWN0X2VuaGFuY2VtZW50Ijp7InN0YXR1cyI6ImdyYW50ZWQiLCJjYW5vbmljYWxQdXJwb3NlcyI6WyJwcm9kX2VuaGFuY2VtZW50Il19fQ%3D%3D; _gid=GA1.2.751268230.1698314109; _scid=367f1f38-7008-46e8-994f-d03fd6061c73; _tt_enable_cookie=1; _ttp=kzw_es9D6Qhn2pFQevNUyW85q4_; viewedSeatgeekEmailModal=true; _sctr=1%7C1698267600000; _swb_consent_=eyJlbnZpcm9ubWVudENvZGUiOiJwcm9kdWN0aW9uIiwiaWRlbnRpdGllcyI6eyJzZWF0Z2Vla19zaXhwYWNrX2lkX2Jhc2VkX2lkZW50aXR5IjoiYWYwODhjMTAtMjNjMi00ZGI0LWE1YTctODlkNDY0NTcyNzA4Iiwic3diX3NlYXRnZWVrX2NvbSI6ImJlNzEzMGJhLTEzMDYtNDhjNC0xZDJkLWM0NDQ4MTE4ODM0MiJ9LCJqdXJpc2RpY3Rpb25Db2RlIjoiZGVmYXVsdCIsInByb3BlcnR5Q29kZSI6InNlYXRnZWVrX2NvbSIsInB1cnBvc2VzIjp7ImFuYWx5dGljcyI6eyJhbGxvd2VkIjoidHJ1ZSIsImxlZ2FsQmFzaXNDb2RlIjoiZGlzY2xvc3VyZSJ9LCJlc3NlbnRpYWxfcHVycG9zZXMiOnsiYWxsb3dlZCI6InRydWUiLCJsZWdhbEJhc2lzQ29kZSI6ImRpc2Nsb3N1cmUifSwicGVyc29uYWxpc2F0aW9uIjp7ImFsbG93ZWQiOiJ0cnVlIiwibGVnYWxCYXNpc0NvZGUiOiJkaXNjbG9zdXJlIn0sInByb2R1Y3RfZW5oYW5jZW1lbnQiOnsiYWxsb3dlZCI6InRydWUiLCJsZWdhbEJhc2lzQ29kZSI6ImRpc2Nsb3N1cmUifX0sImNvbGxlY3RlZEF0IjoxNjk4MzE5MjM4fQ%3D%3D; tracker_device=ee3e5424-1596-4e27-aabf-fce0d210e52c; sg-event-page-view-id=a1116d28-cec9-4ad9-8d3a-2face08d48f8; _scid_r=367f1f38-7008-46e8-994f-d03fd6061c73; _gat_sgGaTracker=1; datadome=1Q3z8s7tFsND8pVHBvEcjaaymLnAbBVBo3agS2QWsDJ4x5Ld99Ik2IYUW54gu3D0lq88QDr_BDFotl4AF~QUodMiQ5ik8jltTJ1_oI2XswFJZlMvKLfPFdOWf~KsRdaN; _ga_44M3TK17XS=GS1.1.1698319238.2.1.1698319402.39.0.0; _ga=GA1.1.531517435.1698314108; IR_20501=1698319402641%7C4523102%7C1698319402641%7C%7C; IR_PI=040e8f64-1bce-11ee-af34-3b90f22b7458%7C1698405802641; _uetsid=bf0b1a1073e511eeb3d9e71113e8925e; _uetvid=bf0b627073e511ee94184fd0e4873797; _dd_s=rum=0&expire=1698320307796"
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
        api_url = "https://seatgeek.com/api/events?page=1&listing_count.gte=1&lat=47.61&lon=-122.33&range=54mi&sort=datetime_local.asc&taxonomies.id=2000000&client_id=MTY2MnwxMzgzMzIwMTU4"
        
        yield scrapy.Request(url=api_url, cookies=self.cookies, callback=self.n_of_pages)

    def n_of_pages(self, response):
        res = json.loads(response.text)
        n_pages= math.ceil(res['meta']['total']/10)
        api_url = "https://seatgeek.com/api/events?page={}&listing_count.gte=1&lat=47.61&lon=-122.33&range=54mi&sort=datetime_local.asc&taxonomies.id=2000000&client_id=MTY2MnwxMzgzMzIwMTU4"
        for i in range(1, n_pages+1):
            yield scrapy.Request(url=api_url.format(i), cookies=self.cookies, callback=self.parse, meta={'pagenum': i}, dont_filter=True)
    def parse(self, response):
        res = json.loads(response.text)
        if response.meta['pagenum'] != res['meta']['page']:
            print(f"API sent page {res['meta']['page']} instead of page {response.meta['pagenum']}")
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
                