# -*- coding: utf-8 -*-
import scrapy
from IsvServiceInfo.items import IsvServiceInfoItem
from scrapy_redis.spiders import RedisSpider
from scrapy_redis import connection
from scrapy.conf import settings

import requests
import re
import datetime
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class IsvServiceInfoSpider(RedisSpider):
    name = "isv_service_info"
    start_urls = [
        'https://fuwu.taobao.com/serv/shop_index.htm?spm=0.0.0.0.CZ3Xrj&page_id=2489&isv_id=45632667&page_rank=2&tab_type=1',
        'https://fuwu.taobao.com/serv/shop_index.htm?spm=0.0.0.0.Oquk72&page_id=678230&isv_id=877021141&page_rank=2&tab_type=1',

'https://fuwu.taobao.com/serv/shop_index.htm?spm=0.0.0.0.mSxKHl&page_id=25995&isv_id=305442977&page_rank=2&tab_type=1',

'https://fuwu.taobao.com/serv/shop_index.htm?spm=0.0.0.0.lH8xCC&page_id=172044&isv_id=570102268&page_rank=2&tab_type=1',

'https://fuwu.taobao.com/serv/shop_index.htm?spm=0.0.0.0.OzhuHM&page_id=690262&isv_id=897211958&page_rank=2&tab_type=1'
        ]
    redis_server = connection.from_settings(settings)

    def parse(self, response):
        print response.url
        item = IsvServiceInfoItem()
        isv_id = re.search('isv_id=(.*?)&', response.url + '&').group(1)
        company_name = response.xpath('//*[@id="seller-header"]/div[1]/div/a/text()').extract()[0]
        servers = response.xpath('//*[@id="searchForm"]/div[2]/table/tbody/tr')
        for server in servers:
            user_number = server.xpath('td[4]/text()').extract()[0]
            browser_number = server.xpath('td[5]/text()').extract()[0]
            item['isv_id'] = isv_id
            item['company_name'] = company_name
            item['user_number'] = user_number
            item['browser_number'] = browser_number
            detail_url = re.sub('service/service.htm', 'ser/detail.html', 'https:' + server.xpath('td[2]/dl/dt/a/@href').extract()[0])
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})
            print detail_url

    def parse_detail(self, response):
        detail_url = response.url
        service_code = re.search('service_code=(.*?)&', detail_url + '&').group(1)
        content = response.xpath('//*[@id="J_SKUForm"]/div[2]/text()')
        # print(content)
        # 判断是否存在"此服务暂不支持在线订购，请您直接联系服务商"
        if not content:
            service_name = response.xpath('//*[@id="J_SKUForm"]/div[1]/h2/text()').extract()[0].replace('\t', '').replace('\n',
                                                                                                                '')
            score = response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/span[2]/text()').extract()[0]
            usability = response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[1]/li[1]/span[2]/@class').extract()[0]
            usability_compare = \
            response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[1]/li[1]/span[2]/text()').extract()[0]
            # 判断是高于还是低于
            if usability == 'low per':
                usability_compare = '-' + usability_compare
            attitude = response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[1]/li[2]/span[2]/@class').extract()[0]
            attitude_compare = \
            response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[1]/li[2]/span[2]/text()').extract()[0]
            if attitude == 'low per':
                attitude_compare = '-' + attitude_compare
            stability = response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[1]/li[3]/span[2]/@class').extract()[0]
            stability_compare = \
            response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[1]/li[3]/span[2]/text()').extract()[0]
            if stability == 'low per':
                stability_compare = '-' + stability_compare

            secure_score = str(
                response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[2]/li[1]/span[2]/text()').extract()[0]).replace(
                '\t', '').replace('\n', '')
            payer_number = response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[2]/li[2]/span[2]/text()').extract()[0]
            nearly_payer_number = \
            response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[2]/li[2]/span[3]/text()').extract()[0]
            continue_rate = response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[2]/li[3]/span[2]/text()').extract()[0]
            refund_rate = response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[2]/li[4]/span[2]/text()').extract()[0]
            open_rate = response.xpath('//*[@id="apc-detail"]/div[2]/div[1]/div[2]/div/ul[2]/li[5]/span[2]/text()')
            # 打开率有点特殊
            if open_rate:
                open_rate = open_rate.extract()[0]
            else:
                open_rate = None
            score_times = re.search('(\d+)',
                                   response.xpath('//*[@id="reviews"]/div[1]/div/div/div[2]/span/text()').extract()[0]).group(1)
            five_score_rate = \
            response.xpath('//*[@id="reviews"]/div[1]/div/div/div[3]/ul/li[1]/span[@class="tb-r-pecent"]/text()').extract()[0].replace('\t', '').replace('\n', '')
            four_score_rate = \
            response.xpath('//*[@id="reviews"]/div[1]/div/div/div[3]/ul/li[2]/span[@class="tb-r-pecent"]/text()').extract()[0].replace('\t', '').replace('\n', '')
            three_score_rate = \
            response.xpath('//*[@id="reviews"]/div[1]/div/div/div[3]/ul/li[3]/span[@class="tb-r-pecent"]/text()').extract()[0].replace('\t', '').replace('\n', '')
            two_score_rate = \
            response.xpath('//*[@id="reviews"]/div[1]/div/div/div[3]/ul/li[4]/span[@class="tb-r-pecent"]/text()').extract()[0].replace('\t', '').replace('\n', '')
            one_score_rate = \
            response.xpath('//*[@id="reviews"]/div[1]/div/div/div[3]/ul/li[5]/span[@class="tb-r-pecent"]/text()').extract()[0].replace('\t', '').replace('\n', '')
            seller_rank_percent_url = 'https://fuwu.taobao.com' + \
                                      response.xpath('//*[@id="desc-log"]/div/div[1]/div[1]/h5/a/@href').extract()[0]
            seller_industry_percent_url = 'https://fuwu.taobao.com' + \
                                          response.xpath('//*[@id="desc-log"]/div/div[1]/div[2]/h5/a/@href').extract()[0]
            # 爬淘宝买家等级占比
            html = requests.get(seller_rank_percent_url).text
            selector = etree.HTML(html)
            seller_rank_percent_trs = selector.xpath('//*[@id="apc-detail"]/div[2]/table/tbody/tr')
            seller_rank_percent = '['
            for seller_rank_percent_tr in seller_rank_percent_trs:
                seller_rank_percent_tds = seller_rank_percent_tr.xpath('td')
                index = 0
                for seller_rank_percent_td in seller_rank_percent_tds:
                    index += 1
                    img = seller_rank_percent_td.xpath('img/@src')
                    if img:
                        seller_rank = re.search('rank/(.*?).gif', img[0]).group(1)
                    else:
                        seller_rank = seller_rank_percent_td.xpath('text()')
                        if seller_rank:
                            seller_rank = str(seller_rank[0]).replace('\t', '').replace('\n', '').replace(' ', '')
                    if seller_rank:
                        if index % 2 == 1:
                            seller_rank_percent = seller_rank_percent + '{\"rank\":\"' + str(seller_rank).replace('\r',
                                                                                                                  '') + '\",'
                        else:
                            seller_rank_percent = seller_rank_percent + '\"percent\":\"' + seller_rank + '\"},'

            seller_rank_percent = seller_rank_percent[:-1] + ']'
            # 爬卖家行业占比
            html = requests.get(seller_industry_percent_url).text
            selector = etree.HTML(html)
            seller_industry_percent_trs = selector.xpath('//*[@id="apc-detail"]/div[2]/table/tbody/tr')
            seller_industry_percent = '['
            for seller_industry_percent_tr in seller_industry_percent_trs:
                seller_industry_percent_tds = seller_industry_percent_tr.xpath('td')
                index = 0
                for seller_industry_percent_td in seller_industry_percent_tds:
                    index += 1
                    img = seller_industry_percent_td.xpath('img/@src')
                    if img:
                        seller_rank = re.search('rank/(.*?).gif', img[0]).group(1)
                    else:
                        seller_rank = seller_industry_percent_td.xpath('text()')
                        if seller_rank:
                            seller_rank = str(seller_rank[0]).replace('\t', '').replace('\n', '').replace(' ', '')
                    if seller_rank:
                        if index % 2 == 1:
                            seller_industry_percent = seller_industry_percent + '{\"industry\":\"' + str(
                                seller_rank).replace(
                                '\r', '') + '\",'
                        else:
                            seller_industry_percent = seller_industry_percent + '\"percent\":\"' + seller_rank + '\"},'

            seller_industry_percent = seller_industry_percent[:-1] + ']'

            # print(company_name)
            print(service_name)
            print(service_code)
            print(score)
            print(usability)
            print(usability_compare)
            print(attitude)
            print(attitude_compare)
            print(stability)
            print(stability_compare)
            print(secure_score)
            print(payer_number)
            print(nearly_payer_number)
            print(continue_rate)
            print(refund_rate)
            print(open_rate)
            print(score_times)
            print(five_score_rate)
            print(four_score_rate)
            print(three_score_rate)
            print(two_score_rate)
            print(one_score_rate)
            # print(seller_rank_percent_url)
            # print(seller_industry_percent_url)
            print(seller_rank_percent)
            print(seller_industry_percent)
            # print(user_number)
            # print(browser_number)

            now_time = datetime.datetime.today()
            item = response.meta['item']
            item['add_time'] = now_time
            item['modify_time'] = now_time
            # item['isv_id'] = isv_id
            # item['company_name'] = company_name
            item['service_name'] = service_name
            item['service_code'] = service_code
            item['score'] = score
            # item['usability'] = usability
            item['usability_compare'] = usability_compare
            # item['attitude'] = attitude
            item['attitude_compare'] = attitude_compare
            # item['stability'] = stability
            item['stability_compare'] = stability_compare
            item['secure_score'] = secure_score
            item['payer_number'] = payer_number
            item['nearly_payer_number'] = nearly_payer_number
            item['continue_rate'] = continue_rate
            item['refund_rate'] = refund_rate
            item['open_rate'] = open_rate
            item['score_times'] = score_times
            item['five_score_rate'] = five_score_rate
            item['four_score_rate'] = four_score_rate
            item['three_score_rate'] = three_score_rate
            item['two_score_rate'] = two_score_rate
            item['one_score_rate'] = one_score_rate
            item['seller_rank_percent'] = seller_rank_percent
            item['seller_industry_percent'] = seller_industry_percent
            # item['user_number'] = user_number
            # item['browser_number'] = browser_number
            yield item


