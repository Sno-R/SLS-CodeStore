import json
import datetime
from flask import Blueprint,url_for,request,render_template,session,redirect
from way_dh_upload_img import dh_upload_img

# 创建了一个蓝图对象
testModule = Blueprint('testModule',__name__)

"""
    GET请求，不带参数
"""
@testModule.route("/get_test1",methods=["GET"])
def get_test1():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': None}
    return json.dumps(return_dict, ensure_ascii=False)


"""
    GET请求，带参数
"""
@testModule.route("/get_test2",methods=["GET"])
def get_test2():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': None}
    # 判断入参是否为空
    if len(request.args) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的params参数
    get_data = request.args.to_dict()
    name = get_data.get('name')
    age = get_data.get('age')
    return_dict['result'] = "%s今年%s岁:%s" %(name,age,datetime.datetime.now())
    # return_dict['result'] = "%s今年%s岁:%s" %(datatrans(request).name,datatrans(request).age,datetime.datetime.now())
    return json.dumps(return_dict, ensure_ascii=False)


"""
    POST请求，带参数
"""

def datatrans(request):
    class data:
        name = request.values.get('name')
        age = request.values.get('age')
        requests = request
    # data.name = request.values.get('age')
    # data.age = request.values.get('name')
    return data

@testModule.route("/post_test1", methods=["POST"])
def post_test1():
    #默认返回内容
    return_dict = {'return_code':'200','return_info':'处理成功','result':None}

    # 判断传入的json数据是否为空
    if len(request.get_data()) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
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
    # return_dict['result'] = dh_upload_img(file, user, pwd, order, reason)
    return_dict['result'] = reason
    return json.dumps(return_dict,ensure_ascii=False)