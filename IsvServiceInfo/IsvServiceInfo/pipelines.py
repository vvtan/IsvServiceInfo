# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
from scrapy.conf import settings
import re
import os


class IsvServiceInfoPipeline(object):
    def __init__(self):
        self.host = os.getenv('POSTGRESQL_HOST')
        self.port = os.getenv('POSTGRESQL_PORT')
        self.user = os.getenv('POSTGRESQL_USER')
        self.password = os.getenv('POSTGRESQL_PASSWORD')
        self.database = os.getenv('POSTGRESQL_DATABASE')

    def process_item(self, item, spider):
        add_time = item['add_time']
        modify_time = item['modify_time']
        isv_id = None
        if item.get('isv_id'):
            isv_id = int(str(item['isv_id']).strip())
        company_name = None
        if item.get('company_name'):
            company_name = str(item['company_name']).strip()
        service_name = str(item['service_name']).strip()
        service_code = str(item['service_code']).strip()
        score = float(str(item['score']).strip())
        usability_compare = self.delete_the_percent(item['usability_compare'])
        attitude_compare = self.delete_the_percent(item['attitude_compare'])
        stability_compare = self.delete_the_percent(item['stability_compare'])
        secure_score = self.delete_the_fen(item['secure_score'])
        payer_number = str(item['payer_number']).strip()
        nearly_payer_number = str(item['nearly_payer_number']).strip()
        continue_rate = self.delete_the_percent(item['continue_rate'])
        refund_rate = self.delete_the_percent(item['refund_rate'])
        open_rate = self.delete_the_percent(item['open_rate'])
        score_times = int(item['score_times'])
        five_score_rate = self.delete_the_percent(item['five_score_rate'])
        four_score_rate = self.delete_the_percent(item['four_score_rate'])
        three_score_rate = self.delete_the_percent(item['three_score_rate'])
        two_score_rate = self.delete_the_percent(item['two_score_rate'])
        one_score_rate = self.delete_the_percent(item['one_score_rate'])
        seller_rank_percent = item['seller_rank_percent']
        seller_industry_percent = item['seller_industry_percent']
        user_number = None
        if item.get('user_number'):
            user_number = int(str(item['user_number']).strip())
        browser_number = None
        if item.get('browser_number'):
            browser_number = int(str(item['browser_number']).strip())

        self.conn = psycopg2.connect(
            host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        self.cursor = self.conn.cursor()
        sql = 'insert into server_info(add_time,modify_time,isv_id,company_name,service_name,service_code,score,usability_compare,attitude_compare,stability_compare,secure_score,payer_number,nearly_payer_number,continue_rate,refund_rate,open_rate,score_times,five_score_rate,four_score_rate,three_score_rate,two_score_rate,one_score_rate,seller_rank_percent,seller_industry_percent,user_number,browser_number) \
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        data = (add_time,modify_time,isv_id,company_name,service_name,service_code,score,usability_compare,attitude_compare,stability_compare,secure_score,payer_number,nearly_payer_number,continue_rate,refund_rate,open_rate,score_times,five_score_rate,four_score_rate,three_score_rate,two_score_rate,one_score_rate,seller_rank_percent,seller_industry_percent,user_number,browser_number)
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            print e
            self.conn.rollback()
            self.cursor = self.conn.cursor()
            sql = 'update  server_info set modify_time=%s, isv_id=%s, company_name=%s, service_name=%s,' \
                  'score=%s, usability_compare=%s, attitude_compare=%s, stability_compare=%s, secure_score=%s,' \
                  'payer_number=%s, nearly_payer_number=%s, continue_rate=%s, refund_rate=%s, open_rate=%s, score_times=%s,' \
                  'five_score_rate=%s, four_score_rate=%s, three_score_rate=%s, two_score_rate=%s, one_score_rate=%s,' \
                  'seller_rank_percent=%s, seller_industry_percent=%s, user_number=%s, browser_number=%s' \
                  ' where service_code = %s  '
            data = (modify_time,isv_id,company_name,service_name,score,usability_compare,attitude_compare,stability_compare,secure_score,payer_number,nearly_payer_number,continue_rate,refund_rate,open_rate,score_times,five_score_rate,four_score_rate,three_score_rate,two_score_rate,one_score_rate,seller_rank_percent,seller_industry_percent,user_number,browser_number,service_code)
            self.cursor.execute(sql, data)
        finally:
            # print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
            self.cursor.close()
            self.conn.commit()
            self.conn.close()

        # print(add_time)
        # print(modify_time)
        # print(isv_id)
        # print(company_name)
        # print(user_number)
        # print(browser_number)
        print(service_name)
        # print(service_code)
        # print(score)
        # print(usability_compare)
        # print(attitude_compare)
        # print(stability_compare)
        # print(secure_score)
        # print(payer_number)
        # print(nearly_payer_number)
        # print(continue_rate)
        # print(refund_rate)
        # print(open_rate)
        # print(score_times)
        # print(five_score_rate)
        # print(four_score_rate)
        # print(three_score_rate)
        # print(two_score_rate)
        # print(one_score_rate)
        # print(seller_rank_percent)
        # print(seller_industry_percent)
        return item

    def delete_the_percent(self, content):
        if content:
            result = re.search('(.*)%', str(content).strip())
            if result:
                # print('delete_the_percent:' + result.group(1))
                return float(result.group(1))
            return 0
        return None

    def get_number(self, content):
        if content:
            result = re.search('(\d+)', str(content).strip())
            if result:
                # print('get_number:' + result.group(1))
                return float(result.group(1))
            return 0
        return None

    def delete_the_fen(self, content):
        if content:
            result = re.search('(.*)分', content)
        if result:
            return float(result.group(1))
        return 0
