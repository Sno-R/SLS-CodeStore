import json
import os
import sys
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
        print(f"配置文件 {filename} 未找到，正在创建...")
        with open(filename, 'w', encoding='utf-8') as file:
            default_config = {}
            json.dump(default_config, file, indent=4, ensure_ascii=False)
        return default_config
    except json.JSONDecodeError:
        print(f"配置文件 {filename} 格式错误")
        return {}


def set_config(_cookies):
    # 修改配置项
    config['cookies'] = _cookies  # 更改设置中的一个选项
    # 将修改后的字典写回JSON文件
    with open('ks_publishing_config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)


# 读取本地图片
def get_all_file_paths(folder_path):
    # 初始化一个空列表来存储所有文件的路径
    all_file_paths = []

    # 使用 os.walk() 遍历指定文件夹及其子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 遍历当前文件夹中的所有文件
        for file in files:
            # 拼接文件的完整路径
            file_path = os.path.join(root, file)
            # 将文件路径添加到列表中
            all_file_paths.append(file_path)

    return all_file_paths



# 选择类目
def push_category(page):
    # 返回旧版
    # page.ele("x://div[@class='style_backOld__1ZyY8']").click()
    # 输入类目
    page.ele("x://input[@class='index_searchInput__2-rbd']").input("手机壳")
    page.wait(2)
    page.ele("手机保护套/壳").click()
    page.wait(2)
    # 点下一步
    page.ele("x://button[@class='ecom-g-btn ecom-g-btn-primary index_nextStep__2t6rM']").click()


# 输入产品参数
def push_title(page, title):

    page.ele('x://input[@placeholder="最多输入30个汉字（60个字符）"]').input(''+'\n')
    page.wait(1)
    page.ele('x://input[@placeholder="最多输入30个汉字（60个字符）"]').input(title)



def push_info(page, param_map):
    page.wait(2)

    eles = page.eles('css:grid-column: span 1')

    # 品牌
    eles[0].ele('css:input').input(param_map['品牌'])
    page.ele('x://div[@class="goods-select-item-option-content"]').wait.displayed()
    page.ele('x://div[@class="goods-select-item-option-content"]').click(by_js=None)
    page.wait(1)

    #功能
    eles[1].ele('css:input').input('其他')
    eles[1]('css:input').wait.displayed()
    page.wait(0.5)
    eles[1]('css:input').input('\n')

    # 适用手机品牌
    eles[2].ele('css:input').input(param_map['适用手机品牌'])
    page.ele(f'x://div[@title="{param_map['适用手机品牌']}"]').wait.displayed()
    page.ele(f'x://div[@title="{param_map['适用手机品牌']}"]').click(by_js=None)


    # 类型
    eles[4].ele('css:input').input(param_map['类型'])
    eles[4].ele('css:input').wait.displayed()
    page.wait(0.5)
    eles[4].ele('css:input').input('\n')

    # 风格
    eles[5].ele('css:input').input(param_map['风格'])
    eles[5].ele('css:input').wait.displayed()
    page.wait(0.5)
    eles[5].ele('css:input').input('\n')

    # 材质
    eles[3].ele('css:input').input(param_map['材质'])
    page.ele('x://div[@class="goods-select-item goods-select-item-option goods-select-item-option-active"]').wait.displayed()
    page.wait(0.5)
    page.ele(
        'x://div[@class="goods-select-item goods-select-item-option goods-select-item-option-active"]').click(by_js=None)


    page.ele('x://input[@placeholder="最多输入30个汉字（60个字符）"]').click()




# 上传白底图
def push_white_background(page, white_path):
    pass






# 上传详情页
def push_details_pic(page, detail_images_paths):
    # page.ele('x://button[@class="kpro-seller-material-upload-btn"]').click()
    page.wait(1)
    page.ele('x://button[@class="kpro-seller-material-upload-btn"]/preceding-sibling::input[1]').input(detail_images_paths)


#发货时间
def push_delivery_time(page,ship_time):
    page.wait(1)
    page.ele("价格库存").click()
    radio_input = page.eles(
        """x://div[@data-b-form-item[contains(., '{"key":"delivery_delay_day","label":"价格库存_现货发货时间"}')]]//input[@type='radio' and @class='ecom-g-radio-input']""")
    # 次日发[0]
    # 48小时[1]
    # 当日发[2]

    if ship_time == 48:
        # print("48小时发货")
        radio_input[1].check()
    if ship_time == 24:
        # print("24小时当日发货")
        radio_input[2].check()

#上传sku图片
def push_sku_pic(page,img_path):
    #########################上传sku图片
    page.ele("x://div[@id='skuValue-颜色分类']//div[@class='upload_button__17N5e']").click(by_js=None)
    # page.wait(1)
    page.wait.ele_loaded(
        "x://div[contains(@data-b-relation-ship, '价格库存_商品规格_操作按钮')]//label[contains(@class, 'upload_actionBefore__eqMCw')]//input[@type='file']")  # 等待 id 为 div1 的元素加载
    # print('加载出现')
    upload = page.ele(
        "x://div[contains(@data-b-relation-ship, '价格库存_商品规格_操作按钮')]//label[contains(@class, 'upload_actionBefore__eqMCw')]//input[@type='file']")

    upload.input(img_path)
    # page.wait(1)



#图片重命名
def rename_image(folder_path, original_name, new_name):

    # 构造原始和新的文件路径
    original_path = os.path.join(folder_path, original_name)
    new_path = os.path.join(folder_path, new_name)

    # 检查原始文件是否存在
    if os.path.exists(original_path):
        try:
            # 重命名文件
            os.rename(original_path, new_path)
            return new_path
        except Exception as e:
            return new_path


        # 重命名文件
        # os.rename(original_path, new_path)
        # return new_path
    else:
        return "错误：指定的文件不存在"






#上传sku规格2
def push_sku2(page,specifications_list2):
    page.ele('添加规格类型(1/3)').click(by_js=None)
    page.ele('x://input[@placeholder="下拉选择或自定义输入" and @value=""]').input('型号\n')


    for _list in specifications_list2:
        # print("规格2",_list)
        page.wait(0.5)
        page.ele('x:(//div[@class="goods-row HmFJWqLMexomvCkuqXR6 specLine"][last()]//input[@placeholder="请输入自定义规格值"])[last()]').input(_list+'\n')







def push_suk(page,sku_list,sku_img_path):

    page.wait(1)
    page.ele("价格库存").click()
    page.wait(1)

    # sku
    page.ele('x://div[@class="goods-col goods-col-6"]/button').click()
    page.wait(1)
    page.ele('x://input[@placeholder="下拉选择或自定义输入"]').input('款式\n')
    page.wait(1)
    # page.ele('x:(//input[@placeholder="请输入自定义规格值"])[last()]').input("苹果" + "\n")
    # page.wait(1)



    #sku属性
    for _list in sku_list:

        color_sku = _list.split("->")
        sku_name = color_sku[0]
        #sku属性
        # print("sku属性",sku_name)
        #sku url
        sku_img_name = color_sku[1].split("/")[-1]
        # print("sku路径",sku_img_path)
        sku_img_path_name = sku_img_path +"\\" +sku_img_name
        # print("sku图片名--1->",sku_img_path_name)
        #修改图片名字
        result = rename_image(sku_img_path, sku_img_name, sku_name+".jpg")
        # print(result)


        page.ele('x:(//input[@placeholder="请输入自定义规格值"])[last()]').input(sku_name+"\n")
        page.wait(1)
        # 添加图片
        page.ele("x:(//div[@class='crd_f4GtCj5DDlHD_Skc uploadBtn']/preceding-sibling::input[1])[last()]").input(result)

        #上传sku 图片
        # push_sku_pic(page, sku_img_path_name)

    page.wait(1)



def push_price_inventory(page,price,inventory):
    page.wait(2)
    page.ele('x://input[@placeholder="总库存"]').input(inventory)
    page.ele('x://input[@placeholder="价格"]').input(price)

    page.ele('批量设置').click(by_js=None)



#第一步传主图
def push_main_pic(page, main_images_paths):

    if "https://s.kwaixiaodian.com/zone/goods/config/release/add" not in page.url:
        page.get("https://s.kwaixiaodian.com/zone/goods/config/release/add")


    # 发送图片文件上传设置要上传的文件路径
    # 第一步
    # 触发上传主图

    page.ele('x://div[@class="JYmB5tXIR_uNCGUkMjen"]').click(by_js=None)

    upload = page.eles('tag:input@type=file')

    # print("主图本地地址",main_images_paths)
    # 传入多个路径，批量上传主图
    upload[0].input(main_images_paths)

    index_recomtag = page.ele("手机/数码/电脑办公 > 手机/配件 > 手机壳",timeout=6)
    if index_recomtag:
        # print("智能自动类型匹配到")
        page.wait(1)
        index_recomtag.click(by_js=None)
    else:
        page.wait(1)
        page.ele("x://input[@class='goods-select-selection-search-input']").input("手机壳")
        page.wait(1)
        page.ele('手机/数码/电脑办公 > 手机/配件 > 手机壳').click(by_js=None)


    page.wait(1)
    # 点下一步
    page.ele("下一步，完善商品信息").click(by_js=None)


# 继续发布
def continue_publishing(page):
    page.wait(1)
    page.ele("提交审核").click()

    page.wait.load_start()
    # 继续发布
    page.get('https://s.kwaixiaodian.com/zone/goods/config/release/add')

#上传状态
def continue_publishing_status(id,status,goods_id,conten):

    url = "https://www.hongtudz.cn/rpa/api/publish/update"

    params = {
        'id': id,
        'status': status,
        'conten': conten,
        # 'goodsId': goods_id
    }

    response = requests.post(url, params=params)
    data = response.json()
    print("======》",data)
    # print(data['code'])

    #{"msg":"修改成功","code":0}
    return data['code']


def ks_login(page):
    # print(page.url)
    if page.url == "chrome://newtab/":
        page.get("https://login.kwaixiaodian.com/?biz=openshop_pc&source=PC2023guanwang&channel=undefined&redirect_url=https://s.kwaixiaodian.com/zone/store/create/guide?source=PC2023guanwang")
        # 获取当前url
        url = page.url
        print(url)
        page.wait(2)

        if "https://login.kwaixiaodian.com/" in page.url:
            # print("检测到您还未登录，请您先登录，在进行操作")
            logger.info("检测到您还未登录，请您先登录，在进行操作")
            input('登录完成后输入任意键继续')
        elif "https://s.kwaixiaodian.com/zone/home" in page.url:
            logger.info("已检测到页面,请确保账号属于登录状态进行下一步操作")
            # print("已检测到页面,请确保账号属于登录状态进行下一步操作")

        # return "请登录"

    elif "https://login.kwaixiaodian.com/" in page.url:
        # print("检测到您还未登录，请您先登录，在进行操作")
        logger.info("检测到您还未登录，请您先登录，在进行操作")
        input('登录完成后输入任意键继续')
    elif "https://s.kwaixiaodian.com/zone/home" in page.url:
        # print("已检测到页面,请确保账号属于登录状态进行下一步操作")
        logger.info("已检测到页面,请确保账号属于登录状态进行下一步操作")
    else:
        page.get('https://s.kwaixiaodian.com/zone/goods/config/release/add')
        # print("当前游览器地址", page.url)

    # 取cookies
    # _cookies = page.cookies()
    # print(_cookies)

    # jsessionid_cookie = next((cookie for cookie in _cookies if cookie['name'] == 'PHPSESSID'), None)
    # print("cookie------",jsessionid_cookie)

    # 设置配置项cookie
    # set_config(jsessionid_cookie)





def main():
    # 以该配置创建页面对象
    page = ChromiumPage()
    page.set.auto_handle_alert()

    # if cookies:
    #     page.set.cookies(cookies)

    ks_login(page)

    #####################################################

    user_id = ht_user
    logger.success(f'尊敬的【{user_id}】VIP用户,欢迎使用鸿图抖音商品自动上架程序')
    shop_id = ht_user
    shop_type = "快手"
    shop_name = ""
    shop_name_list =[]

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

        logger.info(f"当前任务平台类型为{platform_type}")

        data_items_list = data['data']['dataItems']
        # print(data_items_list)

        ship_time = data['data']['shipTime']
        # print("发货时间", ship_time)

        # 循环任务
        for data_items in data_items_list:

            # print("循环任务--->",len(data_items_list),data_items)

            stak_id = data_items['id']
            # print("stak_id-----", stak_id)

            title = data_items['title']
            # print("标题", title)

            sku_prices = data_items['skuPrices'][0]
            # print(sku_prices)
            # 库存
            inventory = sku_prices['quantity']
            # print("库存",inventory)
            # 价格
            price = sku_prices['price']
            # print("价格",price)

            main_pic_list = data_items['mainPic'].split(",")
            # print("主图---",len(main_pic_list), main_pic_list)

            detail_pic_list = data_items['detailPic'].split(",")
            # print("详情页",len(detail_pic_list), detail_pic_list)

            param_map = data_items['paramMap']
            # print(param_map)

            # sku
            specifications_list = data_items['specifications']['款式'].split(",")
            # print(specifications_list)

            # sku手机型号
            specifications_list2 = data_items['specifications']['型号'].split(",")
            # print("=====", specifications_list2)

            main_img_path = f"快手自动上架图片\\{title}\\主图"
            detail_img_path = f"快手自动上架图片\\{title}\\详情页"
            sku_img_path = f"快手自动上架图片\\{title}\\sku"

            print("主图路径", main_img_path)
            print("详情页路径", detail_img_path)
            print("sku路径", sku_img_path)

            # 主图下载
            main_pic_full_urls = main_pic_list
            detail_pic_full_urls = detail_pic_list

            logger.info("数据解析中...请稍等")

            sku_list_pic = []
            for i in specifications_list:
                sku_list_pic.append(i.split("->")[1])



            # 下载主图图片到本地
            # download_images(main_pic_full_urls, main_img_path)
            # 创建下载器对象
            d1 = DownloadKit(main_img_path)
            for i in main_pic_full_urls:
                d1.add(i, file_exists='skip')

            d1.wait()

            logger.success("主图获取完成【ok】")

            # 下载详情页图片到本地 读取本地路径
            # download_images(detail_pic_full_urls, detail_img_path)
            # 创建下载器对象
            d2 = DownloadKit(detail_img_path)
            for i in detail_pic_full_urls:
                d2.add(i, file_exists='skip')

            d2.wait()

            logger.success("详情页图获取完成【ok】")


            # 下载sku图片到本地
            sku_pic_full_urls = sku_list_pic
            # download_images(sku_pic_full_urls, sku_img_path)
            # 创建下载器对象
            d3 = DownloadKit(sku_img_path)
            for i in sku_pic_full_urls:
                d3.add(i, file_exists='skip')
            d3.wait()
            logger.success("sku图片获取完成【ok】")

            # 读取本地路径
            # sku_images_paths = list_files_in_folder(sku_img_path)

            detail_images_paths = list_files_in_folder(detail_img_path)

            # 读取本地路径
            main_images_paths = list_files_in_folder(main_img_path)

            print("主图路径list-----", main_images_paths)

            #####################################################

            # start_time = time.time()  # 记录开始时间
            #
            push_main_pic(page, main_images_paths)
            logger.success("上传主图 选择类目【ok】")

            # if page.ele('x://div[@id="kpro-tool-box-tools-containner"]'):
            #     print('删除元素')
            #     page.remove_ele(page.ele('x://div[@id="kpro-tool-box-tools-containner"]'))

            push_info(page, param_map)
            logger.success("设置参数【ok】")

            push_title(page, title)
            logger.success("设置标题【ok】")

            # push_white_background(page, main_images_paths[-1])
            # logger.success("白底图上传处理【ok】")

            push_details_pic(page, detail_images_paths)
            logger.success("详情页图片上传ok")

            # # push_delivery_time(page, ship_time)
            # # logger.success('设置发货时间【ok】')

            push_suk(page, specifications_list, sku_img_path)
            logger.success("设置参数sku【ok】")

            push_sku2(page, specifications_list2)
            logger.success("设置sku参数2【ok】")

            push_price_inventory(page, price, inventory)
            logger.success("设置价格库存【ok】")

            continue_publishing(page)
            logger.success("完成发布【ok】")

            goods_id = "0000001"
            ret_status = continue_publishing_status(stak_id, 1, goods_id, "上传成功")

    logger.info('任务已全部完成无新任务,请在鸿图定制小程序内选择您要发布的商品')
    input("请按任意键退出")
    exit()




if __name__ == "__main__":
    config = load_config('ks_publishing_config.json')
    # cookies = config.get('cookies')
    ht_user = config.get('鸿图账号')
    print("鸿图账号----->",ht_user)

    main()