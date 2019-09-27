#!/bin/sh
echo $(date)
echo "Running Cron"
cd /root/nodoron_scrapy/
/root/venev/bin/python -m scrapy crawl yad2_rent
