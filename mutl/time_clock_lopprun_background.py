import datetime
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
import time


def clock(num):
    print('now time:', datetime.datetime.now(), 'process:', num)

def test_add_run(scheduler):
    scheduler.add_job(clock, 'date', run_date = datetime.datetime.now() + datetime.timedelta.seconds(1), args=[i])

job_id_list =[]

if __name__ == '__main__':
    # print(datetime.datetime.now())
    scheduler = BackgroundScheduler()
    # for i in range(1,3):
    #     job_id_list.append(scheduler.add_job(clock, "interval", seconds=3, args=[i]).id)

    for i in range(1,3):
        job_id_list.append(scheduler.add_job(test_add_run, "interval", seconds=3, args=[scheduler,i]).id)
        
    scheduler.start()

    time.sleep(10)
    scheduler.remove_job(job_id=job_id_list[0])    

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


# from apscheduler.schedulers.background import BackgroundScheduler
# import datetime

# def clock(num):
#     print('now time:', datetime.datetime.now(), 'process:', num)

# if __name__ == '__main__':
#     scheduler = BackgroundScheduler()
#     for i in range(1, 3):
#         # 注意这里 clock 函数后面没有括号，因为我们只是传递函数引用，而不是调用它
#         scheduler.add_job(clock, "interval", seconds=3, args=(i,))
        
#     scheduler.start()

#     # 为了防止脚本退出，我们使用一个无限循环
#     try:
#         while True:
#             pass
#     except (KeyboardInterrupt, SystemExit):
#         scheduler.shutdown()