# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
import MySQLdb
import time
import sys
import random
reload(sys)
sys.setdefaultencoding("utf-8")

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
        title = '\'' + item['title'] + '\''
        print title
        content = '\'' + item['content'] + '\''
        isTop = 0
        date = item['date']
        the_time = time.mktime(time.strptime(date, '%Y-%m-%d'))
        website = item['website']
        level = item['level']
        type = item['type']
        level_type = '[' + level + ']' + type
        self.db = MySQLdb.connect("localhost", "root", "twwtww", "javachina",charset="utf8")
        print item['url']
        self.post.update({'url': item['url']}, {'$set': dict(item)},True)
        cursor = self.db.cursor()
        sql_for_nid = 'SELECT nid from t_node where title = %s' % str('\''+ level_type + '\'')
        print sql_for_nid
        cursor.execute(sql_for_nid)
        nid = cursor.fetchone()
        if not nid:
            nid = 52
        else:
            nid = nid[0]
        nid = random.randint(51, 64)
        print nid
        sql = ("insert into t_topic(uid, nid, title, content, is_top, create_time, update_time, status) values(%d, %d, %s, %s, %d, %d, %d, %d)" %
               (int(uid), int(nid), str(title), str(content), isTop, the_time, the_time, 1))
        # print sql

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 发生错误时回滚
            print '回滚回滚回滚'
            self.db.rollback()

        # 关闭数据库连接
        self.db.close()
        print('已爬取条数:' + str(self.post.count()))
        return item


