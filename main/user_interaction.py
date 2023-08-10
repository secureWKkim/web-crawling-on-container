import sys
from crawling import crawl_data_to_insert
from write_db import store_crawled_data_psql


# TODO: dic, global func 사용
class UserInteraction:
    def __init__(self, my_scheduler):
        self.my_scheduler = my_scheduler
        self.input = sys.stdin.readline
        self.process_option_input(self.input().strip())

    def process_option_input(self, option):
        if option == 'c':
            self.alter_crawling_job_options()
        elif option == 'w':
            self.alter_write_db_job_options()
        elif option == 'a':
            self.my_scheduler.stored_jobs()
        # elif option == 'k':
        #     self.pause_specific_job()
        elif option == 's':
            self.my_scheduler.shutdown()
        elif option == 'e':
            print("Program Exit...")
            self.my_scheduler.shutdown()  # 이렇게 안하면 s옵션 실행 후 e옵션 실행하게 되면 scheduler is not running 에러가 발생하기 때문에.
            exit()  # 이것만 갖고도 되는지 불확실
        else:
            print("Oops, There's something wrong with input...\n")

    def alter_crawling_job_options(self):
        schedule_type, seconds = self.return_args()
        self.my_scheduler.set_crawling_interval(seconds)
        self.my_scheduler.remove_all_jobs()
        # self.my_scheduler.remove_job('1')  # WARN: sometimes it returns LookUpError so try not to use
        self.my_scheduler.schedule(crawl_data_to_insert, schedule_type, '1')
        self.my_scheduler.schedule(store_crawled_data_psql, schedule_type, '2')

    def alter_write_db_job_options(self):
        schedule_type, seconds = self.return_args()
        self.my_scheduler.set_db_write_interval(seconds)
        self.my_scheduler.remove_all_jobs()
        # self.my_scheduler.remove_job('2')
        self.my_scheduler.schedule(crawl_data_to_insert, schedule_type, '1')
        self.my_scheduler.schedule(store_crawled_data_psql, schedule_type, '2')

    def return_args(self):
        print("Choose scheduling type again(cron/interval): ")
        schedule_type = self.input().strip()

        if schedule_type=='interval':
            print("How many seconds do you want to set as scheduling period? ")
            return schedule_type, int(self.input().strip())
        elif schedule_type=='cron':
            print("This Function is not launched yet.")
            return schedule_type, 60



    # def pause_specific_job(self):
    #     print("Which job to pause? 1: crawl, 2: write_db ")
    #     self.my_scheduler.pause_job(self.input().strip())
