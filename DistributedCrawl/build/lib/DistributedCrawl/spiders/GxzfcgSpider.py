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
    name = "gxzfcg_spider"
    name_pre = 'gxzfcg'
    redis_server = connection.from_settings(settings)

    def parse(self, response):
        node_name_pre = settings['NODE_NAME']
        website_pre = '广西壮族自治区政府采购网'
        level_pre = response.xpath('//*[@id="channelBody"]/div[1]/a[2]/text()').extract()[0]
        typr_pre = response.xpath('//*[@id="channelBody"]/div[1]/a[3]/text()').extract()[0]
        ul = response.xpath("//*[@id=\"channelBody\"]/div[2]/ul/li")
        for li in ul:
            item = TenderItem()
            item['node_name'] = node_name_pre
            item['website'] = website_pre
            item['level'] = level_pre
            item['type'] = typr_pre
            item['title'] = li.xpath("a/@title").extract()[0]
            item['date'] = li.xpath("span[@class=\"date\"]/text()").extract()[0]
            item['url'] = 'http://www.gxzfcg.gov.cn' + li.xpath("a/@href").extract()[0]
            article = newspaper.Article(
                'http://www.gxzfcg.gov.cn' + li.xpath("a/@href").extract()[0],
                language='zh', fetch_images=False)
            article.download()
            article.parse()
            item['content'] = article.text
            # 生成时间
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['add_time'] = now_time
            item['update_time'] = now_time
            # print(item)
            yield item
