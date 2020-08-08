# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from collections import defaultdict
import json

class MagazineToJsonPipeline:
    def open_spider(self, spider):
        self.magazines = defaultdict(list)

    def close_spider(self, spider):
        with open("magazines.json", "w", encoding="utf-8") as f:
            f.write(json.dumps([self.magazines], ensure_ascii = False, indent = 4))

    def process_item(self, item, spider):
        self.magazines[item["from_url"]].append({
                                                    "name": item["name"], 
                                                    "link": item["link"],
                                                    "scanned_by": item["scanned_by"]
                                                })
        return item