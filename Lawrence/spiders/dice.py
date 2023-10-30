import scrapy
import json

class DiceSpider(scrapy.Spider):
    name = "dice"
    BASE_URL = "https://dice.fm"
    headers = {'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en',
            'Connection': 'keep-alive',
            'Content-Length': '92',
            'Content-Type': 'application/json',
            'Host': 'api.dice.fm',
            'Origin': 'https://dice.fm',
            'Referer': 'https://dice.fm/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76',
            'X-Api-Timestamp': '2021-10-06',
            'X-Client-Timezone': 'Africa/Cairo',
            'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
    custom_settings = {
        'ROBOTSTXT_OBEY': True
    }

    def start_requests(self):
        request = scrapy.FormRequest(
            url="https://api.dice.fm/unified_search",
            formdata={"count":"24","lat":"47.6062","lng":"-122.3321","cursor":"g3QAAAABZAAEcGFnZWEB","tag":"music:gig"},
            headers=self.headers,
            callback=self.parse_response,
        )

        yield request

    def parse_response(self, response):
        yield {'res': response.text}
        
        # res = json.loads(response.text)
        # yield res
