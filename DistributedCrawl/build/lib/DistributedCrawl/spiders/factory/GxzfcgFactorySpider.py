# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import newspaper
import redis
from DistributedCrawl.items import TenderItem
from scrapy_redis.spiders import RedisSpider
from scrapy_redis import connection
from scrapy.conf import settings


class GxzfcgFactorySpider(RedisSpider):
    name = "gxzfcg_factory"
    name_pre = 'gxzfcg'
    # allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.gxzfcg.gov.cn/CmsNewsController/recommendBulletinList/channelCode-cgxx/20/page_1.html"
        ]
    redis_server = connection.from_settings(settings)

    def parse(self, response):
        level_xpaths = [
            "//*[@id=\"bodyMain\"]/div/aside/div/nav/ul/li[1]/ul/li",
            "//*[@id=\"bodyMain\"]/div/aside/div/nav/ul/li[2]/ul/li"
        ]
        level_names = [
            "区本级采购",
            "市(县)级采购"
        ]
        i = 0
        for level_xpath in level_xpaths:
            level_name = level_names[i]
            i += 1
            ul = response.xpath(level_xpath)
            for li in ul:
                item = TenderItem()
                item['node_name'] = settings['NODE_NAME']
                item['website'] = '广西壮族自治区政府采购网'
                item['level'] = level_name
                item['type'] = li.xpath("a/text()").extract()[0]
                next_page_url = 'http://www.gxzfcg.gov.cn' + li.xpath("a/@href").extract()[0]
                yield scrapy.Request(next_page_url, callback=self.parse_news, meta={'item': item})

    def parse_news(self, response):
        page_nums = re.search(u'页次：1/(.*?)页', response.xpath("//*[@id=\"QuotaList_paginate\"]/span[1]/text()").extract()[0]).group(1)
        for page_num in range(1, int(page_nums) + 1):
            next_page_url = re.sub('page_(.*?).html', 'page_' + str(page_num) + '.html', response.url)
            self.redis_server.lpush('%s_spider:start_urls' % self.name_pre, next_page_url)
            print next_page_url
        # item = response.meta['item']
        # ul = response.xpath("//*[@id=\"channelBody\"]/div[2]/ul/li")
        # for li in ul:
        #     item['title'] = li.xpath("a/@title").extract()[0]
        #     item['date'] = li.xpath("span[@class=\"date\"]/text()").extract()[0]
        #     item['url'] = 'http://www.gxzfcg.gov.cn' + li.xpath("a/@href").extract()[0]
        #     article = newspaper.Article(
        #         'http://www.gxzfcg.gov.cn' + li.xpath("a/@href").extract()[0],
        #         language='zh')
        #     article.download()
        #     article.parse()
        #     item['content'] = article.text
        #     # 生成时间
        #     now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #     item['add_time'] = now_time
        #     item['update_time'] = now_time
        #     # print(item)
        #     yield item
        # # 下一页
        # if len(response.xpath("//*[@id=\"QuotaList_next\"]")) > 0:
        #     num_str = re.search('page_(.*?).html', response.url).group(1)
        #     num = int(num_str) + 1
        #     next_page_url = re.sub('page_(.*?).html', 'page_' + str(num) + '.html', response.url)
        #     print(next_page_url)
        # if next_page_url:
        #     yield scrapy.Request(next_page_url, callback=self.parse_news)