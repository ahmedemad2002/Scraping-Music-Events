import scrapy
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Lawrence.items import EventItem
import re
import json

class BandsintownSpider(scrapy.Spider):
    name = "bandsintown"
    headers = {
        'Cookie': 'bit_pc=3; bit_hpp=true; bit_geo=%257B%2522name%2522%253A%2522Seattle%252C%2520WA%252C%2520US%2522%252C%2522id%2522%253A5809844%252C%2522city%2522%253A%2522Seattle%2522%252C%2522region%2522%253A%2522Washington%2522%252C%2522region_code%2522%253A%2522WA%2522%252C%2522country%2522%253A%2522United%2520States%2522%252C%2522country_code%2522%253A%2522US%2522%252C%2522latitude%2522%253A47.60621%252C%2522longitude%2522%253A-122.33207%257D; _au_1d=AU1D-0100-001698284212-OK3R19KQ-QVM5; _pbjs_userid_consent_data=3524755945110770; _pubcid=c163eed9-a0c8-4c03-8531-679c3ec6b212; _gid=GA1.2.1880797167.1698284212; _cc_id=5056064ea7629f562e1abcd292663a89; panoramaId=cd36e0240c8e8fa4c90ffc5114e616d53938f43051c4f7e94ce49d6cdfe0af7b; panoramaIdType=panoIndiv; __qca=P0-821682955-1698284213669; _lr_env_src_ats=false; panoramaId_expiry=1698889021327; pbjs-unifiedid=%7B%22TDID%22%3A%224f629299-ef18-42da-90f4-3aeeaf762120%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-10-28T03%3A27%3A27%22%7D; pbjs-unifiedid_last=Sat%2C%2028%20Oct%202023%2003%3A27%3A26%20GMT; _au_last_seen_pixels=eyJhcG4iOjE2OTg0NjM2NDAsInR0ZCI6MTY5ODQ2MzY0MCwicHViIjoxNjk4NDYzNjQwLCJydWIiOjE2OTg0NjM2NDAsInRhcGFkIjoxNjk4NDYzNjQwLCJhZHgiOjE2OTg0NjM2NDAsImdvbyI6MTY5ODQ2MzY0MCwiYWRvIjoxNjk4NDYzNjQzLCJhbW8iOjE2OTg0NjM2NDAsInNvbiI6MTY5ODQ2MzY0Mywib3BlbngiOjE2OTg0NjM2NDMsInNtYXJ0IjoxNjk4NDYzNjQzLCJ1bnJ1bHkiOjE2OTg0NjM2NDAsImJlZXMiOjE2OTg0NjM2NDAsInRhYm9vbGEiOjE2OTg0NjM2NDMsImltcHIiOjE2OTg0NjM2NDMsInBwbnQiOjE2OTg0NjM2NDMsImNvbG9zc3VzIjoxNjk4NDYzNjQzLCJpbmRleCI6MTY5ODQ3MDgxMX0%3D; _csrf=orE82YRBBp9d8PY38_vYUkAn; __gads=ID=d1d96c5ec28cb88d:T=1698284213:RT=1698488124:S=ALNI_MbacVVgFLYpXUtKm4CDjO1AUlv5jg; __gpi=UID=00000cc1c346527d:T=1698284213:RT=1698488124:S=ALNI_MaY78h0f0AW6NbQEja3Yvv3cMUAPQ; cto_bidid=SBEsu19SSmI1bkx1OVA0UU9kMlBjZEpvMUptcXVLdFlCakdpSiUyQmh2WDJ2a3hISWlaMnVKQnJaR1M4Wms1TWpWVUZiV0Rtd3lzV2FDaEwxVkhhWE1ZYU5pckxXMHphRVY5aWUlMkZlWVp4MXNJWVZmUk4lMkZWZkxhZHNwOGhTJTJCT3BVY3p5c3Jp; cto_dna_bundle=h8cJbl80M0RITmhlJTJCZkMwOUJGQlhaMUN2c3hVbzRFRmZnQWxHNHpiUWhZamklMkJsbmV0eWJnNFoxb1lnSzJ4ZFh3NW9TNw; _awl=2.1698488195.5-da6452979c18568671936983c670b696-6763652d6575726f70652d7765737431-0; _ga=GA1.1.1182046754.1698284021; bounceClientVisit6283v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgO6kB0ARgIYB2AJigJY0ID2xNZAxqwLZFUwYALR0qCAKboCAcwk0AThIFDhcxVMz4uVXhID6AMwV9MAEVwBWAOx4AbAFcEvfXrqMH-DGeISK9pxcUVgcFLmVvOD5lXEdnfR1eCCpGGRpzNgh9CQA3eQR7YIUEfQoATyNGMEkFcwA5TwoJWtwAIVZDPFaAJQBlADUABWk7Hhpw4vRvBAUHCRAAGhAFGBBFkEYUfRlWfRQpJlYaGENBfaXN7az9lEPj6FOwfYBfIA; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Oct+28+2023+17%3A12%3A38+GMT%2B0200+(Eastern+European+Standard+Time)&version=202308.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; bounceClientVisit6283=N4IgJglmIFwgTAZnkgDKgjADgGw5YojofCADQgBuUsGOAnFgKypP0AsWziA7D-RUqxQAIwCGAYwDWAMwgAbeQH0wAUwAO8gPYBPALaqAdgBdYMsfIDOqgL4VLNGPCwUZlUzDqNn7bIgpiWrCoFPLqsCAAFsbG6pYApIgAgvHwAGKpaQDuOQB04oZgDiZaWYa5Elp6mRbyALRgYsaqCekA5kYATqo1inUdht0JiGkSYgZKMp1ViQAi8Ew8qTgArsZ6SgaQK9WIs1mqIstrG5ZaK50SPXuRVT3wq+tKY3rqYhBthnPGWupKqpQjMZlmdOsYlCIdJMFM1OnMAHI7ESqOHwABCWhkqTRACUAMoANQACq0cJVDFcwcNZsZOitVOQQGJLMFBOohDB2BRoHBoBROhFGRJ3LQGMxWBwXCA2hIBTAmP4QHpWSB5CLPGKWGw2BQXm8PoYWTBQCgOBhkMJVeqvOLtQJVWJqDyMIIOfAbHZwG00hBOpZjAAZLRiHm0+kUSISSxKMQiAAezX9sAA2gBdGxAA; cto_bundle=FqXbI19nOHE2MEd6N0xmZTMlMkJMRzBnNFNyVlB5WGh5MFBPVkgxc1NjTEJSNndkQzZQNXFMJTJGcmYwbFJqU3ZRcFkzdFpkMlR5bEYlMkZJYmglMkZiMkJhZlpmenl3Z0RsbzNPJTJCYks0dldwWUZFTFZSU2tLM05NR3VKbGcxSDNYenUydTN6REszUVZheDZjdHBjNmwlMkYwT0ZvN1phWUx0clElM0QlM0Q; _ga_7VSQQ2WNWN=GS1.1.1698505948.9.1.1698505965.0.0.0',
    }
    
    event_headers = {'Cookie': 'bit_pc=3; bit_hpp=true; bit_geo=%257B%2522name%2522%253A%2522Seattle%252C%2520WA%252C%2520US%2522%252C%2522id%2522%253A5809844%252C%2522city%2522%253A%2522Seattle%2522%252C%2522region%2522%253A%2522Washington%2522%252C%2522region_code%2522%253A%2522WA%2522%252C%2522country%2522%253A%2522United%2520States%2522%252C%2522country_code%2522%253A%2522US%2522%252C%2522latitude%2522%253A47.60621%252C%2522longitude%2522%253A-122.33207%257D; _au_1d=AU1D-0100-001698284212-OK3R19KQ-QVM5; _pbjs_userid_consent_data=3524755945110770; _pubcid=c163eed9-a0c8-4c03-8531-679c3ec6b212; _gid=GA1.2.1880797167.1698284212; _cc_id=5056064ea7629f562e1abcd292663a89; panoramaId=cd36e0240c8e8fa4c90ffc5114e616d53938f43051c4f7e94ce49d6cdfe0af7b; panoramaIdType=panoIndiv; __qca=P0-821682955-1698284213669; _lr_env_src_ats=false; panoramaId_expiry=1698889021327; pbjs-unifiedid=%7B%22TDID%22%3A%224f629299-ef18-42da-90f4-3aeeaf762120%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-10-28T03%3A27%3A27%22%7D; pbjs-unifiedid_last=Sat%2C%2028%20Oct%202023%2003%3A27%3A26%20GMT; _csrf=orE82YRBBp9d8PY38_vYUkAn; bounceClientVisit6283v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgO6kB0ARgIYB2AJigJY0ID2xNZAxqwLZFUwYALR0qCAKboCAcwk0AThIFDhcxVMz4uVXhID6AMwV9MAEVwBWAOx4AbAFcEvfXrqMH-DGeISK9pxcUVgcFLmVvOD5lXEdnfR1eCCpGGRpzNgh9CQA3eQR7YIUEfQoATyNGMEkFcwA5TwoJWtwAIVZDPFaAJQBlADUABWk7Hhpw4vRvBAUHCRAAGhAFGBBFkEYUfRlWfRQpJlYaGENBfaXN7az9lEPj6FOwfYBfIA; bounceClientVisit6283=N4IgJglmIFwgTAZnkgDKgjADgGw5YojofCADQgBuUsGOAnFgKypP0AsWziA7D-RUqxQAIwCGAYwDWAMwgAbeQH0wAUwAO8gPYBPALaqAdgBdYMsfIDOqgL4VLNGPAEgZlUzDqN4WdtkQUYlqwqBTy6rAgABbGxuqWAKSIAIIJ8ABiaekA7rkAdOKGYA4mWtmGeRJaelkW8gC0YGLGqokZAOZGAE6qtYr1nYY9iYjpEmIGSjJd1UkAIvBMPGk4AK7GekoGkKs1iHPZqiIr65uWWqtdEr37UdW98GsbSuN66mIQ7YbzxlrqSqpKEZjCtzl1jEoRDopgoWl15gA5XYiVTw+AAIS0MjS6IASgBlABqAAU2jgqoZruCRnNjF1VqpyCAxJYQoJ1EIYOwKNA4NAKF1IkyJO5aAxmKwOFgKO0JIKYEwAiA9GyQPJRZ5xSw2GwKK93p9DKyYKAUBwMMhhGqNV4JTqXPIxNReRhBJz4DY7OB2ukIF1LMYADJaMS8ukMihRCSWJRiEQADxaAdgAG0ALo2IA; __gads=ID=d1d96c5ec28cb88d:T=1698284213:RT=1698506785:S=ALNI_MbacVVgFLYpXUtKm4CDjO1AUlv5jg; __gpi=UID=00000cc1c346527d:T=1698284213:RT=1698506785:S=ALNI_MaY78h0f0AW6NbQEja3Yvv3cMUAPQ; cto_bidid=jjTsWV9SSmI1bkx1OVA0UU9kMlBjZEpvMUptcXVLdFlCakdpSiUyQmh2WDJ2a3hISWlaMnVKQnJaR1M4Wms1TWpWVUZiV0Rtd3lzV2FDaEwxVkhhWE1ZYU5pckxUNERIWGliUnNScU4lMkZ4QlRJRHoyUzhvc1dVWkp5OGJLYlE1dU1CalpnWXQ; _au_last_seen_pixels=eyJhcG4iOjE2OTg1MDY3ODYsInR0ZCI6MTY5ODUwNjc4NiwicHViIjoxNjk4NTA2Nzg2LCJydWIiOjE2OTg1MDY3ODYsInRhcGFkIjoxNjk4NTA2Nzg2LCJhZHgiOjE2OTg1MDY3ODYsImdvbyI6MTY5ODUwNjc4NiwiYWRvIjoxNjk4NTA2Nzg2LCJhbW8iOjE2OTg1MDY3ODYsInNvbiI6MTY5ODUwNjc4Niwib3BlbngiOjE2OTg1MDY3ODYsInNtYXJ0IjoxNjk4NTA2Nzg3LCJ1bnJ1bHkiOjE2OTg1MDY3ODYsImJlZXMiOjE2OTg1MDY3ODYsInRhYm9vbGEiOjE2OTg1MDY3ODYsImltcHIiOjE2OTg1MDY3ODYsInBwbnQiOjE2OTg1MDY3ODYsImNvbG9zc3VzIjoxNjk4NTA2Nzg2LCJpbmRleCI6MTY5ODUwNjc4Nn0%3D; cto_dna_bundle=BzOlGV80M0RITmhlJTJCZkMwOUJGQlhaMUN2c3hVbzRFRmZnQWxHNHpiUWhZamklMkJsayUyQnV4S1Y0TU5DVWR6Qk5pNkZFSUFq; cto_bundle=UCLED19UamFBJTJCMlIxZEpxRWpYTFUySmlBdWdYcjN3TmZiYmRJOTF1YnExbTVlcDVWWlVwQTNVSDkzSTdoQzRMMmtuWEdxdUhPSk5ST1ppcEtSTGJrWkxTZE9yd2x6dFRZYW00dnhZTk5VdHRYMHpFd2JYT1UlMkJ0RWczVUg5emgzUGtScHhBd0RaSU5adU5kYWNmMUJkTUIxdWhnJTNEJTNE; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Oct+28+2023+17%3A26%3A28+GMT%2B0200+(Eastern+European+Standard+Time)&version=202308.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; _ga_7VSQQ2WNWN=GS1.1.1698505948.9.1.1698506788.0.0.0; _awl=2.1698506788.5-da6452979c18568671936983c670b696-6763652d6575726f70652d7765737431-0; _ga=GA1.2.1182046754.1698284021; _lr_retry_request=true'}
    
    download_delay = 7
    
    def __init__(self, s_date=None, e_date=None):
        if s_date is None:
            s_date = datetime.now().strftime("%Y-%m-%d")
        if e_date is None:
            e_date = (datetime.strptime(s_date, '%Y-%m-%d') + relativedelta(months=1)).strftime("%Y-%m-%d")
        super(BandsintownSpider, self).__init__()
        self.s_date = s_date
        self.e_date = e_date

    def start_requests(self):
        yield scrapy.Request(f"https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents?came_from=257&utm_medium=web&utm_source=home&utm_campaign=top_event&sort_by_filter=Number+of+RSVPs&concerts=true&date={self.s_date}T00%3A00%3A00%2C{self.e_date}T23%3A00%3A00&page=1&longitude=-122.33207&latitude=47.60621", callback=self.parse_urls)

    def parse_urls(self, response):
        res = json.loads(response.text)
        events = res['events']
        for event in events:
            yield scrapy.Request(url=event['callToActionRedirectUrl'], meta={'dt': event['startsAt'], 'venue_name': event['venueName'], 'event_name': event['artistName']}, callback=self.parse, headers=self.event_headers)
        if res['urlForNextPageOfEvents'] is not None:
            yield scrapy.Request(url=res['urlForNextPageOfEvents'], callback=self.parse_urls, headers=self.headers)
    
    def parse(self, response):
        scripts = response.css('script::text').getall()
        ss = [s for s in scripts if s.strip().startswith('window')]
        s = ss[0]
        s = s.strip().replace('window.__data=', '')
        sd = json.loads(s)
        phone = sd['eventView']['body']['venueSectionInfo']['phoneNumber']
        address = sd['jsonLdContainer']['eventJsonLd']['location']['address']
        
        o = EventItem()
        o['event_title'] = response.meta['event_name']
        o['venue_title'] = response.meta['venue_name']
        o['address'] = address['streetAddress']
        o['zip_code'] = address['postalCode']
        o['city'] = address['addressLocality']
        o['state'] = address['addressRegion']
        o['phone_number'] = phone
        o['date'], o['time'] = response.meta['dt'].split('T')
        o['time'] = ':'.join(o['time'].split(':')[:2])
        o['lowest_price'] = o['highest_price'] = None
        o['source_url'] = response.url
        yield o
