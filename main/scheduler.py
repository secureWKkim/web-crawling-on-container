# from apscheduler.jobstores.base import JobLookupError
# Blocking Scheduler 될 수도 있음.
from apscheduler.schedulers.background import BackgroundScheduler
import logging


"""
*코드 출처: https://zzsza.github.io/development/2018/07/07/python-scheduler/
위 코드를 변형해 사용
"""
# REFERENCE: job1 = crawl_data_to_insert, job2 = store_crawled_data_psql"""
class Scheduler:
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.crawling_interval = 60
        self.db_write_interval = 60
        # self.pause_job = {'1': False, '2': False}

    def shutdown(self):  # thread join option is called!
        self.sched.shutdown()
        # print("""If you want to exit program, press 'e' key.
        # If you want to restart scheduler, press 'r' key.""")

    def schedule(self, func, type, job_id):
        if type == 'interval':
            self.sched.add_job(func, type, seconds=self.crawling_interval if job_id=='1' else self.db_write_interval, id=job_id)
            # self.sched.add_job(func, type, seconds=seconds, id=job_id)
        elif type == 'cron':
            self.sched.add_job(func, type, day_of_week='mon-sun',
                               hour='0-23', second='*/2', id=job_id)
        elif type=='listener':
            self.sched.add_listener(func)

    def set_crawling_interval(self, new_interval):
        if self.crawling_interval != new_interval:
            logging.info("Successfully change crawling interval")
        self.crawling_interval = new_interval

    def set_db_write_interval(self, new_interval):
        if self.db_write_interval != new_interval:
            logging.info("Successfully change DB-write interval")
        self.db_write_interval = new_interval

    def remove_all_jobs(self, job_id=None):
        # If I use remove_job method, sometimes it returns JobLookupError(no job_id) so I changed to use remove_all_jobs method.
        self.sched.remove_all_jobs()

        # self.sched.remove_job()
        # self.pause_job[job_id] = True
        # try:
        #     self.sched.remove_job(job_id)
        # except JobLookupError as err:
        #     logging.error("fail to stop Scheduler: {err}".format(err=err))
        #     return

    def stored_jobs(self):
        # self.sched.print_jobs()
        print(self.sched.get_jobs())

    # def modify_job_option(self, job_id, type, args):
    #     if type == 'interval':
    #         self.sched.modify_job(type, id=job_id, seconds=args['seconds'])
    #     elif type == 'cron':
    #         self.sched.modify_job(type, id=job_id, day_of_week='mon-sun',
    #                            hour='0-23', second='*/2')

        # self.sched.modify_job(job_id=job_id, type=type, args=args)

    # def hello(self, type, job_id):
    #     print("%s Scheduler process_id[%s] : %d" % (type, job_id, time.localtime().tm_sec))

