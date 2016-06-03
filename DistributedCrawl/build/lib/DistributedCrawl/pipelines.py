# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
import MySQLdb
import time

class DistributedcrawlPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        uid = 26
        title = item['title']
        content = item['content']
        isTop = 0
        date = item['date']
        the_time = time.mktime(time.strptime(date, '%Y-%m-%d'))
        website = item['website']
        level = item['level']
        type = item['type']
        level_type = '[' + level + ']' + type
        self.db = MySQLdb.connect("localhost", "root", "twwtww", "javachina")
        print item['url']
        self.post.update({'url': item['url']}, {'$set': dict(item)},True)
        cursor = self.db.cursor()
        sql_for_nid = 'SELECT nid from t_node where title = %s' % level_type
        nid = 51
        sql = ("insert into t_topic(uid, nid, title, content, is_top, create_time, update_time, status) values(%s, %s, %s, %s, %s, %s, %s, %s)" %
               (uid, nid, title, content, isTop, the_time, the_time, 1))

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()

        # 关闭数据库连接
        self.db.close()
        print('已爬取条数:' + str(self.post.count()))
        return item


