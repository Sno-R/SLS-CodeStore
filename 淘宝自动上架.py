import sys
import json
import os
import requests
from DrissionPage import ChromiumPage
from loguru import logger
from DownloadKit import DownloadKit

# 移除默认的日志处理器
logger.remove()

# 定义一个更美观的日志格式
format_ = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "  # 时间显示为绿色
    "<level>{level: <8}</level> | "                # 级别，左对齐，确保对齐美观
    # "<yellow>{thread.name: <8}</yellow> | "       # 线程名显示为黄色，左对齐，宽度为18
    "<cyan>{elapsed}</cyan> - "                    # 经过的时间显示为青色
    "<level>{message}</level>"                     # 消息内容，根据级别显示不同颜色
)

# 添加自定义的日志处理器，输出到标准错误流，使用上面定义的格式
logger.add(sys.stderr, format=format_)


def download_images(image_urls, folder_path):
    # 检查文件夹是否存在，如果不存在则创建
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    downloaded_files = []

    for image_url in image_urls:
        # 提取图片文件名
        image_name = image_url.split('/')[-1]

        # 下载图片
        response = requests.get(image_url)
        if response.status_code == 200:
            file_path = os.path.join(folder_path, image_name)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            downloaded_files.append(file_path)

    return downloaded_files


def list_files_in_folder(folder_path):
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path)]




def load_config(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.info(f"配置文件 {filename} 未找到，正在创建...")
        with open(filename, 'w', encoding='utf-8') as file:
            default_config = {}
            json.dump(default_config, file, indent=4, ensure_ascii=False)
        return default_config
    except json.JSONDecodeError:
        logger.info(f"配置文件 {filename} 格式错误")
        return {}


def set_config(_cookies):
    # 修改配置项
    config['cookies'] = _cookies  # 更改设置中的一个选项
    # 将修改后的字典写回JSON文件
    with open('tb_publishing_config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)





# 输入产品参数
def push_title(page,title):
    # 输入标题 商品标题最多填写30个汉字（60个字符）
    page.ele('xpath://input[@placeholder="最多允许输入30个汉字（60字符）"]').input(title)



def push_info(page,param_map,sybrand,model_name):

    # 品牌
    page.ele('xpath://*[@id="struct-p-20000"]//input').input("OTHER/其他\n")
    page.wait(0.5)

    if '流行元素' in param_map:
        # # 流行元素
        page.wait(0.5)
        page.ele('x://*[@id="struct-p-231100582"]//input').input(param_map['流行元素'])



    if '保护套质地' in param_map:
        # # 保护套质地
        page.wait(0.5)
        page.ele('x://*[@id="struct-p-20021"]//input').input(param_map['保护套质地'] + "\n")


    if '型号' in param_map:
        # 型号
        page.wait(0.5)
        page.ele('x://*[@id="struct-p-20000~1"]//input').input(param_map['型号'])


    if '风格' in param_map:
        # # 风格
        page.wait(0.5)
        page.ele('x://*[@id="struct-p-20608"]//input').input(param_map['风格'] + "\n")
        page.wait(0.5)

    if '功能' in param_map:
        # # 功能
        page.wait(1)
        function = param_map['功能']
        page.ele('x://*[@id="struct-p-20019"]/div[2]/div[1]/span/span[1]/span[1]/span/input').click(by_js=None)
        page.wait(1)
        page.ele('x://div[@class="options-search"]//input').input(function)
        page.wait(1)
        page.ele(f'x://div[@class="options-item" and @title="{function}"]').click(by_js=None)



    # 款式
    page.ele('x://*[@id="struct-p-122276315"]//input').click(by_js=None)
    page.wait(0.5)
    page.ele('x://div[@class="options-search"]//input').input("保护壳")
    page.wait(0.5)
    page.ele('x://div[@class="options-item" and @title="保护壳"]').click(by_js=None)


    # 适用品牌
    # page.ele('x://*[@id="struct-p-28102"]').click()
    # page.wait(1)
    # page.ele('x://div[@class="options-search"]//input').input(sybrand)
    # page.wait(1)
    # page.ele(f'x://div[@class="options-item" and @title="{sybrand}"]').click(by_js=None)


# 上传主图
def push_main_pic(page, main_images_paths):
    page.wait(0.5)
    page.ele('x:(//div[@class="image-upload-btn"])[1]').click()
    page.wait(1)
    page.ele('x://div[@class="right-btn btn"]').click()

    page.wait(1)

    upload = page('#uploadBtn')

    upload.click.to_upload(main_images_paths)

    pic_len = len(main_images_paths)

    page.ele(f'x:(//div[@class="image-card"])[{pic_len}]')

    logger.info("上传结束")




# 选择类目
def push_category(page):
    # page.get('https://item.upload.taobao.com/sell/merge/category.htm')

    ele_text = page.ele('x:(//*[@class="next-btn next-medium next-btn-primary next-btn-text path-node"])[3]',timeout=5)
    if ele_text.text == "手机保护套/壳":
        logger.info("已自动选择类目")
    else:
        logger.info(ele_text.text)
        page.wait(1)
        page.ele('x:(//*[@class="next-btn next-medium next-btn-primary next-btn-text path-node"])[3]',timeout=5).click()
        page.wait(1)
        page.ele('x://input[@placeholder="类目搜索：可输入产品名称"]').input("手机壳保护壳\n")

        page.wait.ele_loaded('x://div[@class="next-menu-item-inner"]')

        page.ele('x://div[@class="next-menu-item-inner"]').click()
    logger.info("延迟操作")
    # page.wait(1)

    page.ele('确认类目，继续完善').click()

    # page.wait.doc_loaded()
    # logger.info("页面加载完成")
    page.wait.load_start()
    # 执行在新页面的操作
    logger.info(page.title)



def push_details_pic(page,detail_images_paths,detail_pic_full_urls):

    ###点击图片按钮
    page.ele('x:(//div[@class="funcButton--7yBC8"])[1]').click()
    page.wait(0.5)

    ###上传图片
    page.ele('x://div[@class="right-btn btn"]').click()
    page.wait(1)
    upload = page('#uploadBtn')
    # main_images_paths = [r'C:\Users\Administrator\Desktop\拼多多自动上架\20240401193751\主图\1_20231117143927A014.jpg',r'C:\Users\Administrator\Desktop\拼多多自动上架\20240401193751\主图\14黑_20231117143933A015.jpg',r'C:\Users\Administrator\Desktop\拼多多自动上架\20240401193751\主图\14金_20231117143936A016.jpg',r'C:\Users\Administrator\Desktop\拼多多自动上架\20240401193751\主图\14蓝_20231117143938A017.jpg',r'C:\Users\Administrator\Desktop\拼多多自动上架\20240401193751\主图\14紫_20231117143941A018.jpg']
    upload.click.to_upload(detail_images_paths)
    page.wait(3)
    ###上传结束



    #################循环设置suk###################

    #sku属性
    for _list in detail_pic_full_urls:
        #sku url
        img_name = _list.split("/")[-1]
        # logger.info("sku图片名字",img_name)
        # 选取图片元素数组
        # page.wait(1)
        page.ele(f"x://div[@class='items' and @id='items']//div[@title='{img_name}']").click()
        page.wait(1)

    page.ele('x://div[@class="btn btn-blue"]').click()



    #######################################






#上传sku图片
def push_sku_pic_all(page,sku_img_path_name):

    # logger.info("sku------>",sku_img_path_name)
    ##上传sku图片
    ###上传图片
    page.ele('x://div[@class="right-btn btn"]').click(by_js=None)
    page.wait(1)
    upload = page('#uploadBtn')
    # main_images_paths = [r'C:\Users\Administrator\Desktop\拼多多自动上架\20240401193751\主图\1_20231117143927A014.jpg']
    upload.click.to_upload(sku_img_path_name)
    page.wait(1)
    ###上传结束





def push_suk(page,sku_list,sku_img_path):

    #sku属性
    for _list in sku_list:

        color_sku = _list.split("->")
        sku_name = color_sku[0]
        #sku属性
        # logger.info("sku属性",sku_name)
        #sku url
        sku_img_name = color_sku[1].split("/")[-1]
        # logger.info("sku路径",sku_img_path)
        sku_img_path_name = sku_img_path +"\\" +sku_img_name
        # logger.info("sku图片名",sku_img_path_name)

        page.ele("x:(//span[@class='next-input next-medium color-dropdown-input']/input)[last()]").input(sku_name)
        # page.wait(1)

        # page.ele('颜色名称最大长度为130个字符(65个汉字)').click()

        # #选择添加sku图片
        page.ele('x:(//button[@class="next-btn next-medium next-btn-normal upload-img-btn"])[last()]').click()
        page.wait(1)
        # 上传sku 图片
        push_sku_pic_all(page,sku_img_path_name)

        page.wait(1)

        # 新增规格项
        ele_button = page.ele('x:(//button[@class="next-btn next-medium next-btn-normal next-btn-text add"])[2]')
        ele_button.wait.displayed()
        ele_button.click()
        page.wait(1)



def find_img_name(page,img_name):

    # logger.info("图片名字",img_name)

    #选取图片元素数组
    # page.wait(2)
    page.ele(f"x://div[@class='items' and @id='items']//div[@title='{img_name}']").click()
    page.wait(0.5)
    page.ele('x://div[@class="btn btn-blue"]').click()



def push_sku2(page,specifications_list2,sybrand):


    page.wait(2)
    page.ele('x://span[@class="next-input next-medium sell-cascader-select-sale-props-item color-sub-items should-hidden-border-left"]//input').input(sybrand)
    page.wait(2)
    #一级选择
    page.ele('x://ul[@class="next-menu next-ver next-cascader-menu"]/li[@class="next-menu-item next-cascader-menu-item"]').click()
    page.wait(1)

    for value in specifications_list2:

        page.ele(f'x://*[@class="next-menu next-ver next-cascader-menu"]//li[@class="next-menu-item next-cascader-menu-item" and .//span[@title="{value}"]]//label').click()
        page.wait(0.5)
    page.ele('销售信息').click()
    page.wait(2)




def push_price_inventory(page,price,inventory):
    page.wait(2)
    page.ele('x://input[@placeholder="价格"]').input(price)
    page.ele('x://input[@placeholder="数量"]').input(inventory)
    page.ele('批量填写').click(by_js=None)
    page.wait(1)
    # page.ele('使用物流配送').click(by_js=None)
    page.ele('x:(//div[@class="sell-transport"]//input)[1]').check()
    #选择物流模板，需要用户填写物流模板
    page.ele('x://span[@class="next-select next-select-trigger next-select-single next-medium transport-select next-inactive next-has-search"]//input').input("广东\n")


#发货时间
def push_delivery_time(page,ship_time):
    #label[1] label[2] label[3]


    if ship_time == 48:
        logger.info("48小时发货")
        page.ele('48小时内发货').click()
    else:
        logger.info("24小时当日发货")
        page.ele('24小时内发货').click()



def tb_login(page):

    if page.tabs_count > 1:
        page.close_tabs(others=page.get_tab())

    if page.url == "chrome://newtab/":
        page.get("https://qn.taobao.com/home.htm/SellManage/all?current=1&pageSize=20")
        page.wait.load_start()

        if "mms.pinduoduo.com/login" in page.url:
            logger.info("检测到您还未登录，请您先登录，在进行操作")
            input('登录完成后输入任意键继续')
        elif "item.upload.taobao.com/sell/merge/category" in page.url:
            logger.info("已检测到页面,请确保账号属于登录状态进行下一步操作")

    elif "mms.pinduoduo.com/login" in page.url:
        logger.info("检测到您还未登录，请您先登录，在进行操作")
        input('登录完成后输入任意键继续')
    elif "item.upload.taobao.com/sell/merge/category" in page.url:
        logger.info("已检测到页面,请确保账号属于登录状态进行下一步操作")
    else:
        page.get('https://item.upload.taobao.com/sell/merge/category.htm')
        page.wait.load_start()

        # 取cookies
        # _cookies = page.cookies()
        # jsessionid_cookie = next((cookie for cookie in _cookies if cookie['name'] == 'JSESSIONID'), None)
        # # 设置配置项cookie
        # set_config(jsessionid_cookie)




# 继续发布
def continue_publishing(page):
    page.wait(0.5)

    page.ele("提交宝贝信息").click()
    page.wait(1)

    page.wait.load_start()
    #继续发布
    keep_posting = page.ele("继续发布")
    if keep_posting:
        print("发布成功")
        page.get('https://item.upload.taobao.com/sell/merge/category.htm')




def log_with_time(message):
    logger.info(f" {message}")

# 上传状态
def continue_publishing_status(id, status, goods_id, conten):
    url = "https://www.hongtudz.cn/rpa/api/publish/update"

    params = {
        'id': id,
        'status': status,
        'conten': conten,
        # 'goodsId': goods_id
    }

    response = requests.post(url, params=params)
    data = response.json()
    logger.success(data)

    # {"msg":"修改成功","code":0}
    return data['code']





def main():

    # 以该配置创建页面对象
    page = ChromiumPage(2674)

    page.set.auto_handle_alert()
    # if cookies:
    #     page.set.cookies(cookies)



    tb_login(page)


    #####################################################

    user_id = ht_user
    shop_id = ht_user
    shop_type = "淘宝"
    shop_name = ""
    shop_name_list = []

    try:
        response = requests.get(f"https://www.hongtudz.cn/rpa/api/shop/list/{shop_id}")
        response.raise_for_status()

        shop_info_data = response.json()


        for shop_info in shop_info_data['data']:
            if shop_info.get('platformType') == shop_type:
                shop_name = shop_info.get('shopName')
                print(f"店铺名称: {shop_name}")
                shop_name_list.append(shop_name)

        for name in shop_name_list:
            if requests.get(f"https://www.hongtudz.cn/rpa/api/publish/task/{user_id}/{shop_type}/{name}").json()["msg"] == '操作成功':
                shop_name = name


    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")




    count_num = 0

    while requests.get(f"https://www.hongtudz.cn/rpa/api/publish/task/{user_id}/{shop_type}/{shop_name}").json()["msg"] != '任务已全部完成':
        count_num += 1

        data = requests.get(f"https://www.hongtudz.cn/rpa/api/publish/task/{user_id}/{shop_type}/{shop_name}").json()
        print(data)

        logger.warning(f'第{count_num}次任务自动上架中..')


        platform_type = data['data']['platformType']


        data_items_list = data['data']['dataItems']

        ship_time = data['data']['shipTime']

        # 循环任务
        for data_items in data_items_list:

            stak_id = data_items['id']

            title = data_items['title']

            sku_prices = data_items['skuPrices'][0]
            # 库存
            inventory = sku_prices['quantity']

            # 价格
            price = sku_prices['price']


            main_pic_list = data_items['mainPic'].split(",")

            detail_pic_list = data_items['detailPic'].split(",")

            # 品牌
            sybrand = data_items['syBrand']

            param_map = data_items['paramMap']

            # sku
            specifications_list = data_items['specifications']['颜色分类'].split(",")

            # sku手机型号
            specifications_list2 = data_items['specifications']['适用手机型号'].split(",")


            main_img_path = f"淘宝自动上架图片\\{title}\\主图"
            detail_img_path = f"淘宝自动上架图片\\{title}\\详情页"
            sku_img_path = f"淘宝自动上架图片\\{title}\\sku"

            # 主图下载
            main_pic_full_urls = main_pic_list
            detail_pic_full_urls = detail_pic_list

            log_with_time("数据解析中...请稍等")

            sku_list_pic = []
            for i in specifications_list:
                sku_list_pic.append(i.split("->")[1])



            # 下载主图图片到本地
            # download_images(main_pic_full_urls, main_img_path)
            # # 创建下载器对象
            download_images_d1 = DownloadKit(main_img_path)
            for i in main_pic_full_urls:
                download_images_d1.add(i, file_exists='skip')
            download_images_d1.wait()
            log_with_time("主图获取完成【ok】")


            # 下载详情页图片到本地 读取本地路径
            # download_images(detail_pic_full_urls, detail_img_path)
            # # 创建下载器对象
            download_images_d2 = DownloadKit(detail_img_path)
            for i in detail_pic_full_urls:
                download_images_d2.add(i, file_exists='skip')
            download_images_d2.wait()
            log_with_time("详情页图获取完成【ok】")


            # sku下载
            sku_pic_full_urls = sku_list_pic

            # 下载sku图片到本地
            # download_images(sku_pic_full_urls, sku_img_path)

            # # 创建下载器对象
            download_images_d3 = DownloadKit(sku_img_path)
            for i in sku_pic_full_urls:
                download_images_d3.add(i, file_exists='skip')
            download_images_d3.wait()
            log_with_time("sku图片获取完成【ok】")


            # 读取本地路径
            main_images_paths = list_files_in_folder(main_img_path)
            detail_images_paths = list_files_in_folder(detail_img_path)


            # 读取本地路径
            # sku_images_paths = list_files_in_folder(sku_img_path)
            # logger.info("sku", sku_images_paths)

            #####################################################

            push_main_pic(page, main_images_paths)

            # # #选择类目
            push_category(page)

            push_title(page, title)

            push_info(page, param_map, sybrand, specifications_list2[0])

            # push_details_pic(page, detail_images_paths, detail_pic_full_urls)

            push_sku2(page, specifications_list2, sybrand)

            push_suk(page, specifications_list, sku_img_path)

            push_delivery_time(page, ship_time)
            #
            push_price_inventory(page, price, inventory)

            logger.info("完成发布")

            goods_id = "0000001"
            ret_status = continue_publishing_status(stak_id, 1, goods_id, "上传成功")

            continue_publishing(page)

    logger.info('任务已全部完成无新任务,请在鸿图定制小程序内选择您要发布的商品')
    input("请按任意键退出")



if __name__ == "__main__":
    config = load_config('tb_publishing_config.json')
    cookies = config.get('cookies')
    # logger.info("cookie----->",cookies)
    ht_user = config.get('鸿图账号')
    print("鸿图账号----->",ht_user)

    logger.success(f'尊敬的【{ht_user}】VIP用户,欢迎使用鸿图淘宝商品自动上架程序')

    main()
