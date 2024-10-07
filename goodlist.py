import requests
import pandas as pd

# 1.创建连接对象
# db_config = {
#     'user': 'root',
#     'password': '123456',
#     'host': 'localhost',
#     'database': 'spiders',
#     'port': 3306,
# }
# # 2.创建游标对象
# conn = mysql.connector.connect(**db_config)
# cursor = conn.cursor()


def dh_login(username, password):
    url = "https://shell.obrase.com/hpiApp/web-module/login/verifyUser"

    payload = f"client=web&user={username}&pwd={password}&pati="

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Content-Type': "application/x-www-form-urlencoded",
        'accept-language': "zh-CN,zh;q=0.9",
        'origin': "https://shell.obrase.com",
        'referer': "https://shell.obrase.com/hpiApp/web-isure/security/login/login2.html?loginType=dh&loginOut=true&ver=1632279312060",
        'sec-ch-ua': "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin",
        'x-requested-with': "XMLHttpRequest",
        'Cookie': "_ati=196980620801; ver=hpi; companyId=555313; tfstk=fPRqYE9Lsjh22PvG4g1NLux1te5vX6nInCs1SFYGlijccCNZ73I5cVBsHGVN4hIfhsA6SfR6SGs0GqBwaFxDh1t1iP-wVH7GICs6_VSG2i_sXqBgFwCcBKs1cG5wWHuSAXGBkECOtDiIOwO0vq5Lnobgf8fl5d_Ve0hBkEUlrQgiPXwNhIYXiGxGngVl-gVgoSxGE7bOqSbgiNqozNIlj1X0iacl-wzcoNjmNdYDS77CnmNJ_F2gfybNxEjDlFOuNTyv7gJHLQQ2zMY0K5VMaZWD1nteHL6XIeBpGeGawsTeE_bw622Nb9JMG_AmqXXRId-GyLnaQMJMlpd5FP2DzCSVKIXz87YlMNxGQLnUOZ5XU9R2HVEkoHs2KsL_8mTPLLWdrT4ans9BRCBHijrdV9Qw499qYS-h4ZZOroty6KrgQtbRzMgrr-IYSrjZ-BY4BRBl9aSIlZwTBtbRzMgrzReOEgQPAq_f.; _pati=TOjF27AWQhJQ7zB7bJPbFFFnRcDgurTa; _pati_v=v2"
    }
    response = requests.post(url, data=payload, headers=headers, verify=False)

    cookie_jsessionid = response.cookies['JSESSIONID']
    cookie_companyid = response.cookies['companyId']

    return {
        'JSESSIONID': cookie_jsessionid,
        'companyId': cookie_companyid
    }


def get_goods_data(session, shop_name):
    url = "https://shell.obrase.com/hpiApp/web-module/stock/querySkuToCustom.do"

    payload = f"groupByFields=goodsId&mocName=hpi.module.inventory.SkuToCustom&colIds=&rows=100&page={page}&sidx=&sord=&shopName={shop_name}&searchValue=&isModProperties=0&notDownloadTrade=&outerSkuIdAlias=&outerSkuIdAlias_Empty=&startTime=&endTime=&outerSkuIdAlias_new=&outerSkuId_new=&outerGoodsId_new=&title_new=&goodsId_new=&propertiesName_new=&isShellCustomerClick=1"

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua': "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        'sec-ch-ua-mobile': "?0",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
        'x-requested-with': "XMLHttpRequest",
        'bx-v': "2.5.11",
        'sec-ch-ua-platform': "\"Windows\"",
        'origin': "https://shell.obrase.com",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://shell.obrase.com/hpiApp/web-shell/home2.html",
        'accept-language': "zh-CN,zh;q=0.9",
        'priority': "u=1, i",
        'Cookie': f"JSESSIONID={session}"
    }

    response = requests.post(url, data=payload, headers=headers, verify=False)
    goods_data_json = response.json()

    return goods_data_json


shop_user_list = [
    {"username": "admin591850客服1", "password": "@Aa15118527673", "shop_name": ["拼多多-星星精品数码", "拼多多-星星优品"]},
    {"username": "admin590889-01", "password": "Aw_590889-01", "shop_name": ["拼多多-檬檬潮壳铺",
                                                                             "拼多多-南墙微创A店",
                                                                             "拼多多-GGBOM潮壳",
                                                                             "拼多多-PDD-pdd16090396477",
                                                                             "拼多多-PDD-pdd35879243434",
                                                                             "拼多多-PDD-品悦数码配件专营店",
                                                                             "拼多多-斌斌",
                                                                             "拼多多-斌斌潮壳铺",
                                                                             "拼多多-壳壳主义56",
                                                                             "拼多多-酷机秀潮壳",
                                                                             "拼多多-泡泡骑士66",
                                                                             "拼多多-小杨3C",
                                                                             ]},
    {"username": "admin568872", "password": "Aa123456.", "shop_name": ["PDD-pdd4566515715",
                                                                       "PDD-UJ数码工作室",
                                                                       "PDD-瓜皮数码工作室",
                                                                       "拼多多-pdd-KL",
                                                                       "拼多多-pdd-LJ",
                                                                       "拼多多-pdd-LT",
                                                                       "拼多多-pdd-QZ",
                                                                       "拼多多-PDD-VE",
                                                                       "拼多多-pdd-艾狗",
                                                                       "拼多多-pdd-长顺进口",
                                                                       "拼多多-pdd-长顺数码",
                                                                       "拼多多-PDD-大学生",
                                                                       "拼多多-pdd-灯悦",
                                                                       "拼多多-pdd-枫朗",
                                                                       "拼多多-pdd-伏智手机",
                                                                       "拼多多-pdd-港奈",
                                                                       "拼多多-pdd-谷视",
                                                                       "拼多多-pdd-加立",
                                                                       "拼多多-pdd-健果",
                                                                       "拼多多-pdd-叫米",
                                                                       "拼多多-pdd-劲马",
                                                                       "拼多多-pdd-澜涩",
                                                                       "拼多多-pdd-朗星",
                                                                       "拼多多-pdd-联屯",
                                                                       "拼多多-pdd-麦琦",
                                                                       "拼多多-pdd-曼瑞",
                                                                       "拼多多-pdd-明茹",
                                                                       "拼多多-PDD-缪鸣",
                                                                       "拼多多-PDD-息囊",
                                                                       "拼多多-pdd-相依",
                                                                       "拼多多-pdd-响趣",
                                                                       "拼多多-pdd-星光",
                                                                       "拼多多-pdd-银河",
                                                                       "拼多多-PDD-寓力",
                                                                       "拼多多-pdd-誉选",
                                                                       "拼多多-pdd-月光",
                                                                       "拼多多-pdd99786453622",
                                                                       "拼多多-全的,拼多多-宇宙"
                                                                       ]},
    {"username": "575577Abc-", "password": "Ff-20160401", "shop_name": ["拼多多-潮趣壳"]},
]

all_goods_list = []
list_num = 0

for user_list in shop_user_list:
    session_info = dh_login(user_list['username'], user_list['password'])
    session = session_info['JSESSIONID']
    company_id = session_info.get('companyId', 'default_company_id')  # 使用get方法获取companyId

    # print(user_list, session, company_id)

    for shop_name in user_list['shop_name']:
        page = 1
        while True:
            # print(f"正在获取店铺：{shop_name}, 页码：{page}")
            goods_data_json = get_goods_data(session, shop_name)
            # print(f"商品信息【'{shop_name}': {goods_data_json}】")

            # 检查返回的商品数据是否为空，如果没有商品（rows为空）则跳出当前循环，转到下一个店铺
            if not goods_data_json.get('rows'):
                # print(f"店铺 '{shop_name}' 在第 {page} 页没有更多商品数据")
                break  # 跳到下一个店铺的循环

            
            
            for things in goods_data_json['rows']:
                # print(things)
                all_goods_list.append([])
                for thing in things:
                    # print(thing, things[thing])
                    all_goods_list[list_num].append(things[thing])
                
                list_num += 1


            # list_num += 1
            page += 1  # 页码递增

        print(all_goods_list)





        df = pd.DataFrame(all_goods_list, columns=['gift', 'outerSkuIdAlias', 'parseColorCode', 'goodsId', 'numIid', 'shopName', 'materialCode', 'title', 'propertiesName', "moId","isModProperties","picCode","parseMaterialCode","ecpfId","notDownloadTrade","parseModelCode","outerSkuId","modelCode","colorCode","oldPropertiesName","skuId","parsePicCode","ecpfName"])
        print(df)

        filepath = 'C:/Users/Admintrator/Desktop/testdata.xlsx'
        df.to_excel(filepath, index=False)
        break

            # for i in goods_data_json['rows']:
            #     goodsId = i['goodsId']
            #     shopName = i['shopName']
            #     title = i['title']
            #     outerSkuId = i['outerSkuId']
            #     propertiesName = i['propertiesName']
            #     materialCode = i['materialCode']
            #     print(goodsId, shopName, title, propertiesName, outerSkuId, materialCode)
            #     if all(k in i for k in
            #            ['goodsId', 'shopName', 'title', 'outerSkuId', 'propertiesName', 'materialCode']):
            #         print(goodsId, shopName, title, propertiesName, outerSkuId, materialCode, company_id)

            
            
# # 提交事务
# conn.commit()
# # 清理资源
# cursor.close()
# # 关闭连接
# conn.close()
