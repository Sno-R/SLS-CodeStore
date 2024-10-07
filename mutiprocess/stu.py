import multiprocessing
from DrissionPage import ChromiumOptions, ChromiumPage
import time

co = ChromiumOptions().auto_port()

def drission(user, pwd):
    page = ChromiumPage(ChromiumOptions().auto_port())

    page.get('https://shell.obrase.com/hpiApp/web-isure/security/login/login2.html')

    page.ele('#user').input(user)   # 输入账号
    page.ele('#pwd').input(pwd)  # 输入密码
    page.ele('#loginBtn').click()   # 点击登陆

    time.sleep(10)

    page.close()

    
drission('admin590889-01', 'Aw_590889-01')



if __name__ == "__main__": 

    pool = []
    run_pool = []

    #实例化任务
    for i in range(5):
        p = multiprocessing.Process(target=drission, args=('admin590889-01', 'Aw_590889-01'))
        run_pool.append(p)

    # 启动任务
    for i in run_pool:
        i.start()

    # 等待任务完成
    while True:
        print('pool:',run_pool)
        # mark = 0
        for i in run_pool:
            print(i.is_alive())
            if i.is_alive() == True:
                mark = True
        print('mark:', mark)
        if mark == False:
            print('Done!')
            break
        mark = False
        
        

#     # both processes finished 
#     print("Done!")