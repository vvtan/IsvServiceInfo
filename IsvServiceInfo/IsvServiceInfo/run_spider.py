import scrapy
from spiders.IsvServiceInfoFactorySpider import IsvServiceInfoFactorySpider
from spiders.IsvServiceInfoSpider import IsvServiceInfoSpider
from scrapy.crawler import CrawlerProcess

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
configure_logging()
runner = CrawlerRunner()
runner.crawl(IsvServiceInfoFactorySpider)
runner.crawl(IsvServiceInfoSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until all crawling jobs are finished