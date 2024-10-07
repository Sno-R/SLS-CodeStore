import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


executors = {
    'default':ThreadPoolExecutor(5),
    'processpool':ProcessPoolExecutor(10)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 10
}


import time
from dh_func_mutlprocess import dh_login

def clock(num):
    print('now time:', datetime.datetime.now(), 'process:', num)
    time.sleep(25)

def test_add_run(scheduler, i):
    # 添加一个在1秒后执行的任务
    # scheduler.add_job(clock, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=1), args=(i,), max_instances=5)
    # scheduler.add_job(clock, 'date', run_date=datetime.datetime.now(), args=(i,), max_instances=5)
    scheduler.add_job(dh_login, 'date')

job_id_list =[]

if __name__ == '__main__':
    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
    
    for i in range(1, 3):
        # 添加一个每隔3秒尝试添加任务的定时任务
        job_id_list.append(scheduler.add_job(test_add_run, 'interval', seconds=30, args=(scheduler, i)).id)
        
    scheduler.start()

    # 等待10秒
    time.sleep(10)
    

    try:
        # 保持主线程运行
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        # 关闭调度器
        scheduler.shutdown()