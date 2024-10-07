import datetime
import os
from apscheduler.schedulers.background import BlockingScheduler
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
import time

# DH操作
class dh(object):
    def __init__(self, user, pwd, order_id='', img_path='', afterSale_reason='', afterSale_info='') -> None:
        self.user = user
        self.pwd = pwd
        self.order_id = order_id
        self.img_path = img_path
        self.aftersale_reason = afterSale_reason
        self.aftersale_info = afterSale_info

    def chrome_initialize(self):
        co = ChromiumOptions().auto_port()
        page = ChromiumPage(co)
        return page

    def dh_login(self):    # dh 登陆，需求 dh 账号密码
        page = ChromiumPage()

        page.get('https://shell.obrase.com/hpiApp/web-isure/security/login/login2.html')

        page.ele('#user').input(self.user)   # 输入账号
        page.ele('#pwd').input(self.pwd)  # 输入密码
        page.ele('#loginBtn').click()   # 点击登陆

    def dh_serch_order(self):   # 搜索指定订单，需求订单号
        page = ChromiumPage()

        page.ele('@placeholder=多个逗号分隔').input(self.order_id)   # 输入框填写
        page.ele('@class=el-input-group__append').click(by_js=False)   # 点击查询

    def dh_query_aftersale(self):
        page = ChromiumPage()
        
        page.ele('x://*[@id="orderV2"]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[6]/div/div[2]/button/span[1]').click(by_js=False) # 点击售后
        page.ele('x://*[@id="orderV2"]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[6]/div/div[2]/ul/li[2]/a').click(by_js=False)   # 点击下拉查看售后
        if page.ele('x://*[@id="queryAfterSaleListByTid_0"]/tbody/tr/td', timeout=3):   #等到查询结果元素，并返回查询结果
            return True
        else:
            return False
        
    def download_img_from_diao(self):   # 从数据库下载图片，return 下载后的本地图片地址做成 list 给 dh_upload_img 用，最多3张图
        pass

    def dh_upload_img(self):
        page = ChromiumPage()
        
        page.ele('tag:button@class=btn btn-default btn-xs dropdown-toggle').click(by_js=False) # 点击售后
        page.ele('x://*[@id="orderV2"]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[6]/div/div[2]/ul/li[1]/a').click(by_js=False)   # 点击下拉售后

        page.ele('@placeholder=请填写售后内容').input(self.aftersale_info) # 填写售后信息
        # page.ele('@placeholder=请填写内部备注').input(Internal_Notes) # 填写内部备注

        select = page.ele('@class=form-control pull-left')  # 获取下拉框元素和下拉选项，按照选项value值匹配并选择
        # option = select('t:option')
        select.select.by_value('其他')

        page.ele('@class=btn btn-hpi pull-left').click.to_upload(self.img_path)    # 上传多文件用列表

        page.ele('@text():保存并提交').click()

        os.remove(self.img_path)

    def dh_close_allTabs(self):
        page = ChromiumPage()

        tabs = page.tab_ids
        page.close_tabs(tabs_or_ids=tabs)


# 定时循环任务，获取待处理订单信息
def get_order():
    url = "http://115.231.97.229:6001/Api/GetDy_AfterSales_Reasons.ashx"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'accept-language': "zh-CN,zh;q=0.9",}
    
    response = requests.post(url,headers=headers, verify=False)
    return response.json()['AfterLists']

# 任务成功，回传数据
def send_result(db_id):
    url = "http://115.231.97.229:6001/Api/UpDate_DY_OrderAfterStatues.ashx"

    payload=f'id={db_id}'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'accept-language': "zh-CN,zh;q=0.9",}

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

# 下载订单图片
def download_img(url):
    # url = url
    respone = requests.get(url)
    # print(respone.content)

    desktop_path = os.path.expanduser("~/Desktop")+'/临时图片.jpg'

    with open(desktop_path, 'wb') as f:
        f.write(respone.content)
    
    return desktop_path

# 循环任务
def loop_mission():
    order_info = get_order()
    print(order_info)
    if order_info != []:
        for order in order_info:
            db_id = order['id']
            order_id = order['OrderSn']
            img_download_path = order['AfterSales_Image']
            aftersale_info = order['Reamrk']
            aftersale_reason = order['AfterSales_Reasons']
            dh_username = order['Pxoxy_AccName']
            dh_pwd = order['Pxoxy_Pwd']
            print(f'数据库ID：{db_id}，订单ID：{order_id}，图片路径：{img_download_path}，售后信息：{aftersale_info}，售后原因：{aftersale_reason}，多鸿账号：{dh_username}，多鸿密码：{dh_pwd}')
            
            img_path = download_img(img_download_path)
            
            dh_process = dh(dh_username, dh_pwd, order_id=order_id, img_path=img_path, afterSale_info=aftersale_info)
            dh_process.chrome_initialize()
            dh_process.dh_login()
            dh_process.dh_serch_order()
            dh_process.dh_query_aftersale()
            dh_process.dh_upload_img()
            dh_process.dh_close_allTabs()
            send_result(db_id)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(loop_mission, "interval", seconds=30)
    scheduler.start()
    