import os
import time

if __name__ == '__main__':
    while True:
        os.system('cd /root/nodoron_scrapy && /root/venev/bin/python -m scrapy crawl yad2_rent')
        print("Done, going to sleep")
        time.sleep(60 * 60)

