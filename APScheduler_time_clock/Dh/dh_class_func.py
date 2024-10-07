from DrissionPage import WebPage
import os


class dh(object):
    def __init__(self, user, pwd, order_id='', img_path='', afterSale_reason='', afterSale_info='') -> None:
        self.user = user
        self.pwd = pwd
        self.order_id = order_id
        self.img_path = img_path
        self.aftersale_reason = afterSale_reason
        self.aftersale_info = afterSale_info

    def dh_login(self):    # dh 登陆，需求 dh 账号密码
        page = WebPage('d')

        page.get('https://shell.obrase.com/hpiApp/web-isure/security/login/login2.html')

        page.ele('#user').input(self.user)   # 输入账号
        page.ele('#pwd').input(self.pwd)  # 输入密码
        page.ele('#loginBtn').click()   # 点击登陆

    def dh_serch_order(self):   # 搜索指定订单，需求订单号
        page = WebPage('d')

        page.ele('@placeholder=多个逗号分隔').input(self.order_id)   # 输入框填写
        page.ele('@class=el-input-group__append').click()   # 点击查询

    def dh_query_aftersale(self):
        page = WebPage('d')
        
        page.ele('x://*[@id="orderV2"]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[6]/div/div[2]/button/span[1]').click() # 点击售后
        page.ele('x://*[@id="orderV2"]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[6]/div/div[2]/ul/li[2]/a').click()   # 点击下拉查看售后
        if page.ele('x://*[@id="queryAfterSaleListByTid_0"]/tbody/tr/td', timeout=3):   #等到查询结果元素，并返回查询结果
            return True
        else:
            return False
        
    def download_img_from_diao(self):   # 从数据库下载图片，return 下载后的本地图片地址做成 list 给 dh_upload_img 用，最多3张图
        pass

    def dh_upload_img(self):
        page = WebPage('d')
        
        page.ele('tag:button@class=btn btn-default btn-xs dropdown-toggle').click() # 点击售后
        page.ele('x://*[@id="orderV2"]/div[1]/div/div[2]/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[6]/div/div[2]/ul/li[1]/a').click()   # 点击下拉售后

        page.ele('@placeholder=请填写售后内容').input(self.aftersale_info) # 填写售后信息
        # page.ele('@placeholder=请填写内部备注').input(Internal_Notes) # 填写内部备注

        select = page.ele('@class=form-control pull-left')  # 获取下拉框元素和下拉选项，按照选项value值匹配并选择
        option = select('t:option')
        select.select.by_value(self.aftersale_reason)

        page.ele('@class=btn btn-hpi pull-left').click.to_upload(self.img_path)    # 上传多文件用列表

        page.ele('@text():保存并提交').click()

        os.remove(self.img_path)

        # return '上传完毕'

    def dh_close_allTabs(self):
        page = WebPage('d')

        tabs = page.tab_ids
        page.close_tabs(tabs_or_ids=tabs)

    

def test_dh():
    job = dh(user='admin590889-01', pwd='Aw_590889-01', order_id='240905-556101803551871')
    job.dh_login()
    job.dh_serch_order()
    # query_result = job.dh_query_aftersale()
    # if query_result == True:
    #     print('无售后记录')
    #     job.dh_upload_img
    # else:
    #     print('有售后')
    
    job.dh_close_allTabs


# if __name__ == '__main__':
    # a = dh(user='admin590889-01', pwd='Aw_590889-01', order_id='240905-556101803551871')
    # a.dh_login()
    # a.dh_serch_order()
    # a.dh_query_aftersale()
    # if a.dh_query_aftersale() == True:
    #     print('无售后记录')
    #     a.dh_upload_img
    # else:
    #     print('有售后')





    
    
# dh_login('admin590889-01', 'Aw_590889-01')
# dh_serch_order('240905-556101803551871')
# dh_query_aftersale()
# print(dh_query_aftersale())


