# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EventItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    event_title = scrapy.Field()
    venue_title = scrapy.Field()
    address = scrapy.Field()
    zip_code = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    phone_number = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    lowest_price = scrapy.Field()
    highest_price = scrapy.Field()
    source_url = scrapy.Field()
