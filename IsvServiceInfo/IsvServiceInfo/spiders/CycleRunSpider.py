# -*- coding: utf-8 -*-
import scrapy
import re
import codecs
import datetime
import redis
import requests
from lxml import etree
import random
import time
from IsvServiceInfo.items import IsvServiceInfoItem
from scrapy_redis.spiders import RedisSpider
from scrapy_redis import connection
from scrapy.conf import settings
import time
import sched
from IsvServiceInfoSpider import IsvServiceInfoSpider
from datetime import date, datetime, timedelta


class IsvServiceInfoFactorySpider(RedisSpider):
    name = "cycle_run"
    start_urls = [
        'https://fuwu.taobao.com/serv/shop_index.htm?spm=0.0.0.0.CZ3Xrj&page_id=2489&isv_id=45632667&page_rank=2&tab_type=1']
    redis_server = connection.from_settings(settings)

    def parse(self, response):
        self.runTask(self.work, hour=4)

    def work(self):
        self.redis_server.lpush('isv_service_info_factory:start_urls', 'https://fuwu.taobao.com/serv/shop_index.htm?spm=0.0.0.0.CZ3Xrj&page_id=2489&isv_id=45632667&page_rank=2&tab_type=1')
        print "更新周期到"

    def runTask(self, func, day=0, hour=0, min=0, second=0):
        # Init time
        now = datetime.now()
        strnow = now.strftime('%Y-%m-%d %H')
        # print "now:", strnow
        # First next run time
        period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
        next_time = now + period
        strnext_time = next_time.strftime('%Y-%m-%d %H')
        # print "next run:", strnext_time
        while True:
            # Get system current time
            iter_now = datetime.now()
            iter_now_time = iter_now.strftime('%Y-%m-%d %H')
            if str(iter_now_time) == str(strnext_time):
                # Get every start work time
                # print "start work: %s" % iter_now_time
                # Call task func
                func()
                # print "task done."
                # Get next iteration time
                iter_time = iter_now + period
                strnext_time = iter_time.strftime('%Y-%m-%d %H')
                # print "next_iter: %s" % strnext_time
                # Continue next iteration
                continue
            # 1分钟检查一次
            time.sleep(600)

        # runTask(work, min=0.5)
