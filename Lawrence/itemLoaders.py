import scrapy
from scrapy.loader import ItemLoader
from Lawrence.items import EventItem

class EventItemLoader(ItemLoader):
    default_item_class = EventItem
