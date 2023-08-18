# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from typing import OrderedDict

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ConcatenateDescriptionPipeline(object):
    def process_item(self, item, spider):
        # using xpath to select every text content of the <p> and <li> elements in the description
        combined_text = "\n".join(x.xpath("string()").get().strip() for x in item["description"])
        item["description"] = combined_text
        return item


class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('Products.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=False) + "\n"  #
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
