from DrissionPage import ChromiumOptions, ChromiumPage
import os
import time

# page.get('https://shell.obrase.com/hpiApp/web-isure/security/login/login2.html')




def dh_login():    # user, pwd,,dh 登陆，需求 dh 账号密码
    page = ChromiumPage(ChromiumOptions().auto_port())

    page.get('https://shell.obrase.com/hpiApp/web-isure/security/login/login2.html')
    
    time.sleep(3)
    page.close()
    # page.ele('#user').input(user)   # 输入账号
    # page.ele('#pwd').input(pwd)  # 输入密码
    # page.ele('#loginBtn').click()   # 点击登陆

dh_login()
# dh_login('admin590889-01', 'Aw_590889-01')
# dh_serch_order('240905-556101803551871')
# dh_query_aftersale()
# print(dh_query_aftersale())

