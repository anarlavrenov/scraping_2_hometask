# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from hashlib import md5


class EpicentrparserPipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client.goods

    def process_item(self, item, spider):

        item['_id'] = self.hash_id(item)

        collection = self.mongobase['epicentr']
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            pass

        return item

    def hash_id(self, item):
        bytes_input = str(item).encode('utf-8')

        return md5(bytes_input).hexdigest()


class EpicentrPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item