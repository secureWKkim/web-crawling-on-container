import time
import logging

from ..logger import setLogOptions
from ..scheduler import Scheduler

from ..crawling import crawl_data_to_insert
from ..write_db import store_crawled_data_psql

my_scheduler = Scheduler()


def initialize_scheduler():
    my_scheduler.schedule(crawl_data_to_insert, 'interval', '1')
    my_scheduler.schedule(store_crawled_data_psql, 'interval', '2')


def return_my_scheduler():
    return my_scheduler


if __name__ == '__main__':  # 얘만 도커 파일 바깥으로 빠져야 될지도...?
    setLogOptions()
    initialize_scheduler()
    try:
        while True:  # Keep the main thread alive
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Exit Program by KeyboardInterrupt.")
