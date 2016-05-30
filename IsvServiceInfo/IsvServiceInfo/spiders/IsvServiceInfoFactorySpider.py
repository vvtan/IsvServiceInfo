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
from IsvServiceInfoSpider import IsvServiceInfoSpider


class IsvServiceInfoFactorySpider(RedisSpider):
    name = "isv_service_info_factory"
    start_urls = [
        'https://fuwu.taobao.com/serv/shop_index.htm?spm=0.0.0.0.CZ3Xrj&page_id=2489&isv_id=45632667&page_rank=2&tab_type=1']
    redis_server = connection.from_settings(settings)
    count = 0

    def parse(self, response):
        self.redis_server.delete('isv_service_info:items')
        self.redis_server.delete('isv_service_info:dupefilter')
        self.redis_server.delete('isv_service_info:start_urls')
        f = codecs.open('service-code-list.csv', 'r', 'utf-8')
        for datas in f.readlines():
            data = datas[:-1].split(',')
            print data[1]
            self.generate_url(data[0])
        f.close()

    def generate_url(self, service_code):
        self.count = 0
        # 随机休眠0~1秒
        time.sleep(random.random())
        url = 'https://fuwu.taobao.com/ser/detail.html?service_code='
        url += service_code
        html = requests.get(url).text
        selector = etree.HTML(html)
        company_url = selector.xpath('//*[@id="apc-detail"]/div[1]/div/div/p[1]/a/@href')
        # 防止没有公司服务列表只有服务详细页面
        if not company_url:
            self.redis_server.lpush('isv_service_info:start_urls', url)
            return
        company_url = company_url[0]
        isv_id = re.search('isv_id=(.*?)&', company_url + '&').group(1)
        company_url = 'https://fuwu.taobao.com/serv/shop_index.htm?isv_id='
        company_url += isv_id
        html = requests.get(company_url).text
        selector = etree.HTML(html)
        ul = selector.xpath('//*[@id="seller-header"]/div[2]/div[2]/div/ul/li')
        for li in ul:
            tab_type = li.xpath('span/b/a/text()')[0]
            if '服务列表' == tab_type:
                service_urls = li.xpath('span/b/a/@href')[0]
                service_urls = 'https://fuwu.taobao.com/serv/' + service_urls
                self.redis_server.lpush('isv_service_info:start_urls', service_urls)
                print service_urls
                self.count += 1
                print self.count
                break

