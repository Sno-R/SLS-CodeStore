from DrissionPage import WebPage
import os

# page.get('https://shell.obrase.com/hpiApp/web-isure/security/login/login2.html')


def dh_login(user, pwd):    # dh 登陆，需求 dh 账号密码
    page = WebPage('d')

    page.get('https://shell.obrase.com/hpiApp/web-isure/security/login/login2.html')

    page.ele('#user').input(user)   # 输入账号
    page.ele('#pwd').input(pwd)  # 输入密码
    page.ele('#loginBtn').click()   # 点击登陆

def dh_serch_order(order_id):   # 搜索指定订单，需求订单号
    page = WebPage('d')

    page.ele('@placeholder=多个逗号分隔').input(order_id)   # 输入框填写
    page.ele('@class=el-input-group__append').click()   # 点击查询

def dh_query_aftersale():
    page = WebPage('d')
    
    page.ele('tag:button@class=btn btn-default btn-xs dropdown-toggle').click() # 点击售后
    page.ele('x://*[@id="orderV2"]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[6]/div/div[2]/ul/li[2]/a').click()   # 点击下拉查看售后
    if page.ele('x://*[@id="queryAfterSaleListByTid_0"]/tbody/tr/td', timeout=3):   #等到查询结果元素，并返回查询结果
        return True
    else:
        return False
    
def download_img_from_diao():   # 从数据库下载图片，return 下载后的本地图片地址做成 list 给 dh_upload_img 用，最多3张图
    pass


def dh_upload_img(aftersale_reason, img_file, aftersale_info = '', Internal_Notes = ''):
    page = WebPage('d')
    
    page.ele('tag:button@class=btn btn-default btn-xs dropdown-toggle').click() # 点击售后
    page.ele('x://*[@id="orderV2"]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[6]/div/div[2]/ul/li[1]/a').click()   # 点击下拉售后

    page.ele('@placeholder=请填写售后内容').input(aftersale_info) # 填写售后信息
    page.ele('@placeholder=请填写内部备注').input(Internal_Notes) # 填写内部备注

    select = page.ele('@class=form-control pull-left')  # 获取下拉框元素和下拉选项，按照选项value值匹配并选择
    option = select('t:option')
    select.select.by_value(customer_dh_dict[aftersale_reason])

    page.ele('@class=btn btn-hpi pull-left').click.to_upload(img_file)    # 上传多文件用列表

    page.ele('@text():保存并提交').click()

    for i in img_file:
        os.remove(i)

    return '上传完毕'




# dh_login('admin590889-01', 'Aw_590889-01')
# dh_serch_order('240905-556101803551871')
# dh_query_aftersale()
# print(dh_query_aftersale())

