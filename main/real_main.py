from scheduler import Scheduler

from crawling import crawl_data_to_insert
from write_db import store_crawled_data_psql
from user_interaction import UserInteraction as UI
from logger import setLogOptions

my_scheduler = Scheduler()


def initialize_scheduler():
    my_scheduler.schedule(crawl_data_to_insert, 'interval', '1')
    my_scheduler.schedule(store_crawled_data_psql, 'interval', '2')


if __name__ == '__main__':
    setLogOptions()
    initialize_scheduler()
    while True:
        print(
            """While Program Running, You can choose several options:
                    c: Alter crawling job options (interval)
                    w: Alter DB-write job options (interval)
                    a: Watch current running jobs
                    s: Shutdown Scheduler
                    e: Program Exit
            Tell me any option anytime you want.
            Input Option: """)
        UI(my_scheduler)