#!/bin/bash
scrapy crawl isv_service_info_factory &
scrapy crawl isv_service_info &
supervisord -c ./supervisord.conf
