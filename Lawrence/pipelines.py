# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LawrencePipeline:
    def process_item(self, item, spider):
        return item

class DataProcessingPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        # Basic data cleaning: Removing leading and trailing whitespaces
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = value.strip()

        # Deduplication: Avoiding saving redundant data
        unique_id = item.get("EventTitle", "") + item.get("EventDate", "") + item.get("EventLocation", "")
        # if unique_id in self.ids_seen:
        #     raise DropItem("Duplicate item found: %s" % item)
        # else:
        #     self.ids_seen.add(unique_id)

        # Here, you can add more formatting or processing steps if needed

        return item
