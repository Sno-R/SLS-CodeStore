import datetime
import os
from apscheduler.schedulers.background import BlockingScheduler
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
import time

def dh_upload_img():
    page = ChromiumPage()
    # page.get('https://shell.obrase.com/hpiApp/web-shell/home2.html#/orderV4')
        
    # page.ele('tag:button@class=btn btn-default btn-xs dropdown-toggle').click(by_js=False) # 点击售后
    # page.ele('x://*[@id="orderV2"]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[6]/div/div[2]/ul/li[1]/a').click(by_js=False)   # 点击下拉售后

    # page.ele('@placeholder=请填写售后内容').input(self.aftersale_info) # 填写售后信息
    #     # page.ele('@placeholder=请填写内部备注').input(Internal_Notes) # 填写内部备注

    # # select = page.ele('x://*[@id="showAfterSaleApplyByTid"]/div/div/div[2]/div[2]/select') # 获取下拉框元素和下拉选项，按照选项value值匹配并选择
    # select = page.ele('@class=form-control pull-left')
    # select.select.by_text('其它')
    # print(select)

    # page.ele('@class=btn btn-hpi pull-left').click.to_upload(self.img_path)    # 上传多文件用列表

    page.ele('@text():保存并提交').click()

    # os.remove(self.img_path)

dh_upload_img()