from scrapy_redis import connection
from scrapy.conf import settings
import time

redis_server = connection.from_settings(settings)
redis_server.lpush('isv_service_info_factory:start_urls',
                        'https://fuwu.taobao.com/serv/shop_index.htm?spm=0.0.0.0.CZ3Xrj&page_id=2489&isv_id=45632667&page_rank=2&tab_type=1')
print "更新周期到"
time.sleep(2)