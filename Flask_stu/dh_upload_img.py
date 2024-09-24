from DrissionPage import WebPage


def dh_upload_img(img_filepath, username, password, order_id, aftersale_reson):
    page = WebPage('d')
    page.get('https://shell.obrase.com/hpiApp/web-isure/security/login/login2.html')


    page.ele('#user').input(username)   # 输入账号
    page.ele('#pwd').input(password)  # 输入密码
    page.ele('#loginBtn').click()   # 点击登陆

    page.wait.load_start()  # 等待加载

    # page.ele('@class:layui-layer-btn1').click() # 广告点击关闭

    # page.ele('@class=el-input-group__prepend').next(1).input('240905-556101803551871')    # 定位查询类型找到输入框
    page.ele('@placeholder=多个逗号分隔').input(order_id)   # 输入框填写
    page.ele('@class=el-input-group__append').click()   # 点击查询

    page.wait(1)

    page.ele('tag:button@class=btn btn-default btn-xs dropdown-toggle').click() # 点击售后
    page.ele('tag:a@style=background: transparent; color: rgb(59, 174, 231);').click()  #点击售后下拉

    # page.ele('@placeholder=请填写售后内容').input()   #原因啥的应该不用填
    # page.ele('@placeholder=请填写内部备注').input()

    select = page.ele('@class=form-control pull-left')  # 获取下拉框元素和下拉选项，按照选项value值匹配并选择
    option = select('t:option')
    select.select.by_value(aftersale_reson)

    page.ele('@class=btn btn-hpi pull-left').click.to_upload(img_filepath)    # 上传多文件用列表

    # page.ele('@text():保存并提交').click()  # 点击保存并提交

    # page.quit() # 退出浏览器
    return '上传完成'





