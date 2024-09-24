import schedule
import time
import datetime
import app_loop


def perform_task():
    current_time = datetime.datetime.now()
    print("执行任务:", current_time)

schedule.every(3).seconds.do(perform_task)

now = datetime.datetime.now()
delta = datetime.timedelta(seconds=7)
end = now + delta
# end = datetime.datetime.strptime(f'{now.year}-{now.month}-{now.day} 20:00:00', "%Y-%m-%d %H:%M:%S")

print(now)
print(delta)
# print(target)
print(end)

while True:
    schedule.run_pending()
    # time.sleep(1)
    
    if datetime.datetime.now() > end :
        break


