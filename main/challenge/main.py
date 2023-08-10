# TODO: 중요한 변수들에 Optional 사용
from ..user_interaction import UserInteraction as UI
from init import return_my_scheduler


def main():
    # TODO: 스케줄러에 아래 애들 listener, executor job 으로 넣기
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
        user_interaction = UI(return_my_scheduler())  # Waiting for CLI user input.
        # p: Pause either crawling or DB-write job
        # user_interaction.sense_option_input(sys.stdin.readline().strip())



if __name__ == '__main__':  # 얘만 도커 파일 바깥으로 빠져야 될지도...?
    # Run the scheduled tasks indefinitely
    # import schedule
    # schedule.every().second.do(return_data_to_insert)
    # schedule.every().second.do(store_crawled_data_psql)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    main()