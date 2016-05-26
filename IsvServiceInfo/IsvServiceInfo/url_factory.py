from scrapy_redis import connection
from scrapy.conf import settings


from IsvServiceInfo.spiders import IsvServiceInfoSpider

# scrapy api
from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.conf import settings

def spider_closing(spider):
    """Activates on spider closed signal"""
    log.msg("Closing reactor", level=log.INFO)
    reactor.stop()


# crawl responsibly
settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
crawler = Crawler(settings)

# stop reactor when spider closes
crawler.signals.connect(spider_closing, signal=signals.spider_closed)

crawler.configure()
crawler.crawl(IsvServiceInfoSpider())
crawler.start()
reactor.run()