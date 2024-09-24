import json
import datetime
from flask import Blueprint,url_for,request,render_template,session,redirect
from way_dh_upload_img import dh_upload_img

# 创建了一个蓝图对象
newModule = Blueprint('newModule',__name__)

def opertion(request):
    # 操作分支字典
    pass

@newModule.route("/post", methods=["POST"])
def post():
    #默认返回内容
    return_dict = {'return_code':'200','return_info':'处理成功','result':None}

    # 判断传入的json数据是否为空
    if len(request.get_data()) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    
    action = request.values.get('action')
    order_id = request.values.get('orderid')
    aftersale_reason= request.values.get('reason')
    img_links = request.values.get('imglinks')

    if action == '1':
        print('进入dh_upload_img')
    elif action == '2':
        pass
    


    # name = request.values.get('name')
    # age = request.values.get('age')
    file = request.values.get('file')
    user = request.values.get('user')
    pwd = request.values.get('pwd')
    order = request.values.get('orderid')
    reason = request.values.get('reason')
    print(file,user,pwd,order,reason)
    # # 对参数进行操作
    # return_dict['result'] = "%s今年%s岁:%s" %(name,age,datetime.datetime.now())
    # return_dict['result'] = '%s年%s岁%s' %(datatrans(request).name, datatrans(request).age)
    # dh_test(datatrans(request).name, datatrans(request).age)
    return_dict['result'] = dh_upload_img(file, user, pwd, order, reason)
    
    
    
    
    
    
    
    
    
    
    
    
    return json.dumps(return_dict,ensure_ascii=False)