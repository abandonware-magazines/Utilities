# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from magazine_extractor import settings
from collections import defaultdict
from pathlib import Path
import json, os

OUTPUT_PATH = os.path.join(settings.PROJECT_ROOT, "output")

class MagazineToJsonPipeline:
    def open_spider(self, spider):
        self.magazines = defaultdict(list)

    def close_spider(self, spider):
        Path(OUTPUT_PATH).mkdir(parents = True, exist_ok = True)
        file_path = os.path.join(OUTPUT_PATH, "magazines.json")
        spider.logger.info('Writing results to "%s"', file_path)
        magazines_obj = []
        for magazine_url, magazine_issues in self.magazines.items():
            magazines_obj.append({
                "from_url": magazine_url,
                "name": "",
                "issues": magazine_issues
            })
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(magazines_obj, ensure_ascii = False, indent = 4))

    def process_item(self, item, spider):
        issue_str = ", גליון "
        if issue_str in item["name"]:
            issue = item["name"].partition(issue_str)[-1]
        else:
            issue = item["name"]

        self.magazines[item["from_url"]].append({
                                                    "issue": issue, 
                                                    "link": item["link"],
                                                    "scanned_by": item["scanned_by"]
                                                })
        return item