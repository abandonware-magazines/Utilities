import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MagazineSpider(CrawlSpider):
    name = "magazines"

    custom_settings = {
        'HTTPCACHE_ENABLED': True,
        'ITEM_PIPELINES': {
            'magazine_extractor.pipelines.MagazineToJsonPipeline': 100,
        }
    }

    allowed_domains = ['sites.google.com']

    start_urls = [
        'https://sites.google.com/site/abandonwaremagazines/'
    ]

    rules = [Rule(LinkExtractor(allow='abandonwaremagazines/magazines/'),
                      callback='parse_magazine', follow=True)]

    

    def parse_magazine(self, response):
        trs = response.xpath('//table[@id="goog-ws-list-table"]/tbody/tr')
        for tr in trs:
            if "ydywt-hrwnwt" in response.url:
                yield {
                    "from_url"   : response.url,
                    "name"       : tr.xpath('td[1]/text()').get().replace("\xa0", ""),
                    "link"       : tr.xpath('td[2]/a/@href').get(),
                    "scanned_by" : tr.xpath('td[3]/text()').get().replace("\xa0", "")
                }
            else:
                yield {
                    "from_url"   : response.url,
                    "name"       : tr.xpath('td[1]/a/text()').get(),
                    "link"       : tr.xpath('td[1]/a/@href').get(),
                    "scanned_by" : tr.xpath('td[2]/text()').get().replace("\xa0", "")
                }


"""
[
    { "magazine": "Wiz", "issues": [{"issue": 5, "link": "asdf", "scanned_by": "Yaniv"}] }
]
"""