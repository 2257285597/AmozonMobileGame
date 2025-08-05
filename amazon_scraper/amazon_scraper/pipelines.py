import json
import os
from itemadapter import ItemAdapter

class JsonWriterPipeline:
    def open_spider(self, spider):
        # Don't write anything here since we're using scrapy's -o option
        pass

    def close_spider(self, spider):
        # Don't write anything here since we're using scrapy's -o option
        pass

    def process_item(self, item, spider):
        # Just return the item for scrapy's built-in JSON exporter
        return item
