scrapy crawl isv_service_info -s REDIS_URL=$REDIS_URL
/usr/bin/redis-server
exec "$@"
