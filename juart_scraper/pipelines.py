# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JuartScraperPipeline:
    def process_item(self, item, spider):
        # TODO add a function, that concatenates the description elements in a single string
        return item
