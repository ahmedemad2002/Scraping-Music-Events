import scrapy
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Lawrence.items import EventItem
import re
import json

class BandsintownSpider(scrapy.Spider):
    name = "bandsintown"
    headers = {
        'Cookie': 'bit_pc=3; bit_hpp=true; bit_geo=%257B%2522name%2522%253A%2522Seattle%252C%2520WA%252C%2520US%2522%252C%2522id%2522%253A5809844%252C%2522city%2522%253A%2522Seattle%2522%252C%2522region%2522%253A%2522Washington%2522%252C%2522region_code%2522%253A%2522WA%2522%252C%2522country%2522%253A%2522United%2520States%2522%252C%2522country_code%2522%253A%2522US%2522%252C%2522latitude%2522%253A47.60621%252C%2522longitude%2522%253A-122.33207%257D; _au_1d=AU1D-0100-001698284212-OK3R19KQ-QVM5; _pbjs_userid_consent_data=3524755945110770; _pubcid=c163eed9-a0c8-4c03-8531-679c3ec6b212; _cc_id=5056064ea7629f562e1abcd292663a89; __qca=P0-821682955-1698284213669; _lr_env_src_ats=false; bounceClientVisit6283=N4IgJglmIFwgTAZnkgDKgjADgGw5YojofCADQgBuUsGOAnFgKxaJN0moAs8FlsoAEYBDAMYBrAGYQANjID6YAKYAHGQHsAngFslAOwAusScJkBnJQF8KZmjHgB2CpMpGYdRvCxdsiCsPVYVAoZFVgQAAsDAxUzAFJEAEE4+AAxFNSAd2yAOhE9MFtDdUy9HNF1bQzTGQBaMGEDJXi0gHN9ACclarla9r0u+MRU0WFdeUkOyoSAEXgmBxScAFcDbXldSGWqxBnMpUEl1fWzdWWO0W7diMru+BW1+VHtFWEIVr1Zg3UVeSVKfQGJanDoGeSCTQTWRNDqzABy20ESlh8AAQupJClUQAlADKADUAAotHAVPSXUFDGYGDrLJTkEDCMxBPgqfgwPzgcLQCgdcIM0SuWgMZisdg4CitUR8mBMTnaFkgGRC9wilhseD0CjPV7vPTMmCgFD0HzIARKlUeUUarVK4TUaDuPjs+CWazgVqpCAdMwGAAy6mEjppdIoEVEZnkwkEAA8mr7YABtAC6liAA; __gads=ID=d1d96c5ec28cb88d:T=1698284213:RT=1698905282:S=ALNI_MbacVVgFLYpXUtKm4CDjO1AUlv5jg; __gpi=UID=00000cc1c346527d:T=1698284213:RT=1698905282:S=ALNI_MaY78h0f0AW6NbQEja3Yvv3cMUAPQ; _gid=GA1.2.915803827.1698905283; panoramaId=1fbb6856646161ac621a486d587116d53938641345a1da74534945040602d278; panoramaIdType=panoIndiv; _au_last_seen_pixels=eyJhcG4iOjE2OTg5MDUyODAsInR0ZCI6MTY5ODkwNTI4MCwicHViIjoxNjk4OTA1MjgwLCJydWIiOjE2OTg5MDUyODAsInRhcGFkIjoxNjk4OTA1MjgwLCJhZHgiOjE2OTg5MDUyODAsImdvbyI6MTY5ODkwNTI4MCwiYWRvIjoxNjk4OTA1Mjg0LCJhbW8iOjE2OTg5MDUyODQsInNvbiI6MTY5ODkwNTI4NCwib3BlbngiOjE2OTg5MDUyODQsInNtYXJ0IjoxNjk4OTA1Mjg0LCJ1bnJ1bHkiOjE2OTg5MDUyODAsImJlZXMiOjE2OTg5MDUyODQsInRhYm9vbGEiOjE2OTg5MDUyODQsImltcHIiOjE2OTg5MDUyODAsInBwbnQiOjE2OTg5MDUyODQsImNvbG9zc3VzIjoxNjk4OTA1MjgwLCJpbmRleCI6MTY5ODgxMjEzMX0%3D; _lr_retry_request=true; pbjs-unifiedid=%7B%22TDID%22%3A%22dcffdc26-fe45-433d-9190-6c25f1add5c0%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-11-02T06%3A08%3A04%22%7D; pbjs-unifiedid_last=Thu%2C%2002%20Nov%202023%2006%3A08%3A04%20GMT; panoramaId_expiry=1699510085006; cto_bidid=DUPa319SSmI1bkx1OVA0UU9kMlBjZEpvMUptcXVLdFlCakdpSiUyQmh2WDJ2a3hISWlaMnVKQnJaR1M4Wms1TWpWVUZiV0Rtd3lzV2FDaEwxVkhhWE1ZYU5pckxkVldPOGQzZnVtcE9xSVB3S2k0SWsyWG5velZmelRaTFdQV0ZtdGpQTXZn; cto_dna_bundle=nJSKF180M0RITmhlJTJCZkMwOUJGQlhaMUN2c3hVbzRFRmZnQWxHNHpiUWhZamklMkJsa1lnYVBVQlYlMkJvUURjZCUyRlJNbHhVZ08; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Nov+02+2023+08%3A08%3A42+GMT%2B0200+(Eastern+European+Standard+Time)&version=202308.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; _awl=2.1698905322.5-da6452979c18568671936983c670b696-6763652d6575726f70652d7765737431-0; _ga=GA1.2.1182046754.1698284021; cto_bundle=n9gS-F9XY0JlVkVtWnhYaDNXWlp3YlpBSkxlVDJhR2hEQkYzJTJCVGcyOVFwJTJCSUZPeEhnVjVWV3FqMkxSR1BmJTJCTmM2ME93eHlBSkNETmJVRVBuVGJnR3dJU2ZXUEQxWGglMkJaJTJGdkxITlM1cElDSzU1b3B2aDFyWDh2JTJGYmpMVnBPUDhSNiUyRnl6eGtMWU1uaml5d0dSUCUyQm1hJTJGZ0lIN2clM0QlM0Q; _ga_7VSQQ2WNWN=GS1.1.1698905282.13.1.1698905578.0.0.0; _csrf=RTAgKZk4pSzhwoGU6MNNYsjq',
    }
    
    event_headers = {'Cookie': 'bit_pc=3; bit_hpp=true; bit_geo=%257B%2522name%2522%253A%2522Seattle%252C%2520WA%252C%2520US%2522%252C%2522id%2522%253A5809844%252C%2522city%2522%253A%2522Seattle%2522%252C%2522region%2522%253A%2522Washington%2522%252C%2522region_code%2522%253A%2522WA%2522%252C%2522country%2522%253A%2522United%2520States%2522%252C%2522country_code%2522%253A%2522US%2522%252C%2522latitude%2522%253A47.60621%252C%2522longitude%2522%253A-122.33207%257D; _au_1d=AU1D-0100-001698284212-OK3R19KQ-QVM5; _pbjs_userid_consent_data=3524755945110770; _pubcid=c163eed9-a0c8-4c03-8531-679c3ec6b212; _cc_id=5056064ea7629f562e1abcd292663a89; __qca=P0-821682955-1698284213669; _lr_env_src_ats=false; bounceClientVisit6283=N4IgJglmIFwgTAZnkgDKgjADgGw5YojofCADQgBuUsGOAnFgKxaJN0moAs8FlsoAEYBDAMYBrAGYQANjID6YAKYAHGQHsAngFslAOwAusScJkBnJQF8KZmjHgB2CpMpGYdRvCxdsiCsPVYVAoZFVgQAAsDAxUzAFJEAEE4+AAxFNSAd2yAOhE9MFtDdUy9HNF1bQzTGQBaMGEDJXi0gHN9ACclarla9r0u+MRU0WFdeUkOyoSAEXgmBxScAFcDbXldSGWqxBnMpUEl1fWzdWWO0W7diMru+BW1+VHtFWEIVr1Zg3UVeSVKfQGJanDoGeSCTQTWRNDqzABy20ESlh8AAQupJClUQAlADKADUAAotHAVPSXUFDGYGDrLJTkEDCMxBPgqfgwPzgcLQCgdcIM0SuWgMZisdg4CitUR8mBMTnaFkgGRC9wilhseD0CjPV7vPTMmCgFD0HzIARKlUeUUarVK4TUaDuPjs+CWazgVqpCAdMwGAAy6mEjppdIoEVEZnkwkEAA8mr7YABtAC6liAA; _gid=GA1.2.915803827.1698905283; panoramaId=1fbb6856646161ac621a486d587116d53938641345a1da74534945040602d278; panoramaIdType=panoIndiv; _au_last_seen_pixels=eyJhcG4iOjE2OTg5MDUyODAsInR0ZCI6MTY5ODkwNTI4MCwicHViIjoxNjk4OTA1MjgwLCJydWIiOjE2OTg5MDUyODAsInRhcGFkIjoxNjk4OTA1MjgwLCJhZHgiOjE2OTg5MDUyODAsImdvbyI6MTY5ODkwNTI4MCwiYWRvIjoxNjk4OTA1Mjg0LCJhbW8iOjE2OTg5MDUyODQsInNvbiI6MTY5ODkwNTI4NCwib3BlbngiOjE2OTg5MDUyODQsInNtYXJ0IjoxNjk4OTA1Mjg0LCJ1bnJ1bHkiOjE2OTg5MDUyODAsImJlZXMiOjE2OTg5MDUyODQsInRhYm9vbGEiOjE2OTg5MDUyODQsImltcHIiOjE2OTg5MDUyODAsInBwbnQiOjE2OTg5MDUyODQsImNvbG9zc3VzIjoxNjk4OTA1MjgwLCJpbmRleCI6MTY5ODgxMjEzMX0%3D; _lr_retry_request=true; pbjs-unifiedid=%7B%22TDID%22%3A%22dcffdc26-fe45-433d-9190-6c25f1add5c0%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-11-02T06%3A08%3A04%22%7D; pbjs-unifiedid_last=Thu%2C%2002%20Nov%202023%2006%3A08%3A04%20GMT; panoramaId_expiry=1699510085006; _csrf=RTAgKZk4pSzhwoGU6MNNYsjq; __gads=ID=d1d96c5ec28cb88d:T=1698284213:RT=1698905824:S=ALNI_MbacVVgFLYpXUtKm4CDjO1AUlv5jg; __gpi=UID=00000cc1c346527d:T=1698284213:RT=1698905824:S=ALNI_MaY78h0f0AW6NbQEja3Yvv3cMUAPQ; cto_bidid=myxGjF9SSmI1bkx1OVA0UU9kMlBjZEpvMUptcXVLdFlCakdpSiUyQmh2WDJ2a3hISWlaMnVKQnJaR1M4Wms1TWpWVUZiV0Rtd3lzV2FDaEwxVkhhWE1ZYU5pckxhTGJxRDcwY3llNXk1SENVZnVUMSUyQjFUT0QyYUwwS0xPa3pDdGZ6UXVlTlc; _gat_auPassiveTagger=1; cto_dna_bundle=XY738F80M0RITmhlJTJCZkMwOUJGQlhaMUN2c3hVbzRFRmZnQWxHNHpiUWhZamklMkJsbUlZMmo2Y0ZFMEF5S1RRRmUxQVVZSw; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Nov+02+2023+08%3A17%3A10+GMT%2B0200+(Eastern+European+Standard+Time)&version=202308.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; _awl=2.1698905830.5-da6452979c18568671936983c670b696-6763652d6575726f70652d7765737431-0; _ga=GA1.2.1182046754.1698284021; _ga_7VSQQ2WNWN=GS1.1.1698905282.13.1.1698905831.0.0.0; cto_bundle=XvEBo19Kdmh3JTJGYWpJdUpSbUxVR2c0WVRZc3dOMW5RQTM3SWdVMFhSVWRIYXlOUk5tWlcwdzAzam1MaE42OUFGcjlLTFdobnJUJTJGSW03WjhNU3ppNW56bFJ2WjJtVVJMUVptQ2hMYXJyQ2FmUU5tMHJSODFuSHRRcEFacURlQSUyQkxUbnN6M3pwTUkwcjduWSUyQk1aZjclMkJVNEw1QW9BJTNEJTNE'}
    
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
