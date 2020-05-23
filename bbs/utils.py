from .parameters import CURRENT_USER_ID, CURRENT_USER, DEFAULT_SERVER_ERROR_MESSAGE
from django.shortcuts import reverse, redirect
from functools import wraps
from user.models import User


def restful_response(code, message, data):
    return {'code': code, 'message': message, 'data': data}


def success(message="", data=None):
    return restful_response(200, message, data)


def params_error(message="", data=None):
    return restful_response(200, message, data)


def server_error(message=""):
    return restful_response(code=500, message=message or DEFAULT_SERVER_ERROR_MESSAGE, data=None)


def get_current_user(request):
    '''
    获取当前登录的用户，从session中获取当前用户id，从数据库中查找对应的user返回
    :param request: 请求
    :return: user或None
    '''
    current_user_id = request.session.get(CURRENT_USER_ID)# 检查session中是否存在id
    if current_user_id:
        # 如存在，尝试从数据库中查找user
        try:
            current_user = User.objects.get(id=current_user_id)
            return current_user
        except:
            return None
    else:
        return None

def login_required(func):
    '''
    登录需求装饰器, 对于某些页面, 要求登录后才能访问, 则在视图函数前加上此装饰器
    实现原理为检查session中是否存在当前用户ID, 存在则返回当前函数, 不存在则返回登录页面, 并设置onlogin为true
    注意这里为函数的关键字参数中加入了当前用户，以便于在视图函数中使用
    '''
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        current_user = get_current_user(request)
        if current_user:
            # 如存在，将当前用户加入kwargs中
            kwargs[CURRENT_USER] = current_user
            return func(request, *args, **kwargs)
        else:
            # 如不存在，跳转到登录页面
            return redirect(reverse('user:login'))

    return wrapper