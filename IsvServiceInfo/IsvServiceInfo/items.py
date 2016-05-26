# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IsvServiceInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    add_time = scrapy.Field()
    modify_time = scrapy.Field()
    isv_id = scrapy.Field()
    company_name = scrapy.Field()
    service_name = scrapy.Field()
    service_code = scrapy.Field()
    score = scrapy.Field()
    usability = scrapy.Field()
    usability_compare = scrapy.Field()
    attitude = scrapy.Field()
    attitude_compare = scrapy.Field()
    stability = scrapy.Field()
    stability_compare = scrapy.Field()
    secure_score = scrapy.Field()
    payer_number = scrapy.Field()
    nearly_payer_number = scrapy.Field()
    continue_rate = scrapy.Field()
    refund_rate = scrapy.Field()
    open_rate = scrapy.Field()
    score_times = scrapy.Field()
    five_score_rate = scrapy.Field()
    four_score_rate = scrapy.Field()
    three_score_rate = scrapy.Field()
    two_score_rate = scrapy.Field()
    one_score_rate = scrapy.Field()
    seller_rank_percent = scrapy.Field()
    seller_industry_percent = scrapy.Field()
    user_number = scrapy.Field()
    browser_number = scrapy.Field()
