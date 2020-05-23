# 一些工具函数，实现不同的功能，参看每个函数的注释
from .models import User, Role, TeacherValidationCode, PasswordQuestion, models
from functools import wraps
from django.shortcuts import redirect, reverse
from .parameters import *


# 下面是一组伪restful数据接口，可以规范各个函数之间传递信息的格式
# 参看readme
def restful_response(code, message, data):
    return {'code': code, 'message': message, 'data': data}

def success(message="", data=None):
    return restful_response(200, message, data)

def params_error(message="", data=None):
    return restful_response(400, message, data)

def server_error(message=""):
    return restful_response(code=500, message=message or DEFAULT_SERVER_ERROR_MESSAGE, data=None)



def authentic(username, password):
    '''
    验证用户名和密码是否匹配
    :param username: 要验证的用户名
    :param password: 要验证的密码
    :return: 一个dict，包含状态码code， 信息message和数据data
    '''
    try:
        user = User.objects.get(username=username) # 尝试根据用户名取出用户
    except models.ObjectDoesNotExist:
        user = None
    if user:
        # 如果找到了user，比对密码是否匹配
        if user.password == password:
            # 匹配则返回200及这个user
            return success(data={'user':user})
        else:
            # 不匹配
            return params_error(message='密码错误！')
    else:
        # 根本找不到这个user
        return params_error(message='用户不存在！')


def check_username_unique(username):
    # 检查一个用户名是否唯一（是否已经被某个注册的user占用了）
    try:
        user = User.objects.get(username=username)
    except models.ObjectDoesNotExist:
        user = None

    if user:
        # 已存在同名用户, 用户名不唯一
        return False
    else:
        # 不存在同名用户, 用户名唯一
        return True


def check_teacher_code(teacher_code):
    # 检查一个教师码是否有效
    try:
        # 尝试取出这个教师码
        teacher_code = TeacherValidationCode.objects.get(code=teacher_code)
        # 如果存在，检查是否有效（参看教师码model中的函数）
        if teacher_code.is_validate():
            return True
        else:
            return False
    except models.ObjectDoesNotExist:
        return False


def add_user(username, password, role_name, question_text, answer, teacher_code):
    # 添加一个用户到数据库

    # 首先验证角色和密保问题是否有效
    # 注意这两个参数在前端页面中只能选择不能输入，如果无效输入显然说明内部出现问题
    try:
        role = Role.objects.get(name=role_name)
    except models.ObjectDoesNotExist:
        role = None

    try:
        question = PasswordQuestion.objects.get(text=question_text)
    except models.ObjectDoesNotExist:
        question = None

    if role and question:
        # 角色名和密保问题都有效
        if role.name == '教师':
            # 角色是教师，先检查教师码是否有效
            if check_teacher_code(teacher_code):
                # 检查用户名是否已占用
               if check_username_unique(username):
                   # 添加用户
                   print(question, question_text)
                   User.objects.create(username=username, password=password, role=role, question=question, answer=answer)
                   return success(message='用户添加成功！')
               else:
                   return params_error(message='用户名已被占用！')
            else:
                return params_error(message='教师码无效！')
        elif role.name == '学生':
            # 角色是学生,检查用户名是否已占用
            if check_username_unique(username):
                User.objects.create(username=username, password=password, role=role, question=question, answer=answer)
                return success(message='用户添加成功！')
            else:
                return params_error(message='用户名已被占用！')
    else:
        return server_error()


def login_required(func):
    '''
    登录需求装饰器, 对于某些页面, 要求登录后才能访问, 则在视图函数前加上此装饰器
    实现原理为检查session中是否存在当前用户ID, 存在则返回当前函数, 不存在则返回登录页面,
    并设置error_message作为提示
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
            return redirect(reverse('user:login')+ '?error_message=请先登录！')

    return wrapper


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
        except models.ObjectDoesNotExist:
            return None
    else:
        return None


def recoverPassword(username, question_text, answer, new_password):
    # 首先验证一下username是否存在，还有密保问题
    try:
        user = User.objects.get(username=username)
    except:
        user = None
    try:
        question = PasswordQuestion.objects.get(text=question_text)
    except:
        question = None

    if user:
        if question:
            # 检查密保问题和答案与数据库中user的密保问题和答案是否一致
            if user.question == question and user.answer == answer:
                user.password = new_password
                user.save()
                return success(message='修改成功！')
            else:
                return params_error(message='密保问题或答案错误！')
        else:
            return server_error()
    else:
        return params_error('用户不存在！')

