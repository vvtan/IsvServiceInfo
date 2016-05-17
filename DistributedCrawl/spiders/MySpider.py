from scrapy_redis.spiders import RedisSpider


class MySpider(RedisSpider):
    name = 'myspider'
    start_urls = ['http://www.daomubiji.com/'
                  # 'http://www.daomubiji.com/qi-xing-lu-wang-01.html'
                  ]

    def parse(self, response):
        # do stuff
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")