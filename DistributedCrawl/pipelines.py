# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class DistributedcrawlPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient()

    def process_item(self, item, spider):
        tender = self.connection.TenderInfo.tender
        tender.insert(dict(item))
        print('已爬取条数:' + str(tender.count()))
        return item


