from .parameters import CURRENT_USER_ID, CURRENT_USER, DEFAULT_SERVER_ERROR_MESSAGE
from django.shortcuts import reverse, redirect
from functools import wraps
from user.models import User
from .models import Teacher, Student, Grade, models

# 下面是一组伪restful数据接口，可以规范各个函数之间传递信息的格式
# 参看readme
def restful_response(code, message, data):
    return {'code': code, 'message': message, 'data': data}

def success(message="", data=None):
    return restful_response(200, message, data)

def params_error(message="", data=None):
    return restful_response(200, message, data)

def server_error(message=""):
    return restful_response(code=500, message=message or DEFAULT_SERVER_ERROR_MESSAGE, data=None)


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

def relate_required(func):
    '''
        绑定需求装饰器, 登录需求装饰器的升级版
        对于某些页面, 要求绑定学号/工号后才能访问, 则在视图函数前加上此装饰器
        实现原理为检查session中是否存在当前用户ID, 不存在则返回登录页面，存在则检查是否绑定
        至一个Teacher或Student对象，是则返回当前函数, 否则跳转到绑定界面,
        并设置error_message作为提示
        注意这里为函数的关键字参数中加入了当前用户，以便于在视图函数中使用
        '''
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        current_user = get_current_user(request)
        if current_user:
            # 如存在，将当前用户加入kwargs中
            kwargs[CURRENT_USER] = current_user
            try:
                s = current_user.student
                return func(request, *args, **kwargs)
            except models.ObjectDoesNotExist:
                try:
                    t = current_user.teacher
                    return func(request, *args, **kwargs)
                except models.ObjectDoesNotExist:
                    return redirect(reverse('ems:relate') + '?error_message=请先绑定您的学号或工号！')
        else:
            # 如不存在，跳转到登录页面
            return redirect(reverse('user:login') + '?error_message=请先登录！')
    return wrapper


def current_user_for_template(request):
    # 获取当前登录的用户，传入模板中以便前端界面使用
    # 注意这个方法要加入到setting中的中间件里，这样可以传给前端所有的模板
    current_user = get_current_user(request)
    if current_user:
        return {'current_user': current_user}
    else:
        return {}


def relate(request, id, password):
    # 将当前用户与提交的学号/工号进行关联
    # 1.取出当前用户(如无则返回一个服务器内部错误)
    # 2.根据role, 选择要关联学生还是教师
    # 3.根据id，取出对应的学生或教师（不存在则返回一个参数错误）
    # 4.检查校园卡密码（错误则返回一个参数错误）
    # 5.检查是否已经绑定在某个用户上（是则返回一个参数错误）
    # 6.进行绑定
    current_user = get_current_user(request)
    if not current_user:
        return server_error()
    else:
        if current_user.role.name=='学生':
            try:
                student = Student.objects.get(s_id=id)
            except models.ObjectDoesNotExist:
                return params_error(message='未找到对应的学生信息，请检查学号是否正确！')
            if student.password == password:
                if student.user:
                    return params_error(message='该学号已被绑定，请检查学号是否正确或联系管理员！')
                else:
                    student.user = current_user
                    student.save()
                    return success(message='绑定成功')
            else:
                return params_error(message='密码错误！')
        else:
            try:
                teacher = Teacher.objects.get(t_id=id)
            except models.ObjectDoesNotExist:
                return params_error(message='未找到对应的教师信息，请检查工号是否正确！')
            if teacher.password == password:
                if teacher.user:
                    return params_error(message='该工号已被绑定，请检查工号是否正确或联系管理员！')
                else:
                    teacher.user = current_user
                    teacher.save()
                    return success(message='绑定成功')
            else:
                return params_error(message='密码错误！')


def search_grade1(request, term=None, subject=None):
    # 搜索成绩
    # 首先取出当前登录用户
    current_user = get_current_user(request)

    if not current_user:
        # 没取到说明系统错误（没有登录的人不应该访问到成绩界面）
        return server_error()
    # 先取出所有成绩，不用担心这会影响性能，django中的数据库操作是惰性的，只有真正取值时才会访问数据库
    grades = Grade.objects.all()

    if current_user.role.name == '学生':
        # 如果登录者是个学生，筛选出他自己的成绩（学生不能看别的学生的成绩）
        student = Student.objects.get(user=current_user)
        grades = grades.filter(student=student)

    if term:
        # 如果传入了学期，筛选出该学期的成绩
        grades = grades.filter(subject__term=term)

    if subject:
        # 如果传入了课程，筛选出该课程的成绩
        grades = grades.filter(subject=subject)

    return grades


def search_grade(request, term=None, subject=None):
    # 搜索成绩
    # 首先取出当前登录用户
    current_user = get_current_user(request)
    if not current_user:
        # 没取到说明系统错误（没有登录的人不应该访问到成绩界面）
        return server_error()
    # 先取出所有成绩，不用担心这会影响性能，django中的数据库操作是惰性的，只有真正取值时才会访问数据库
    grades = Grade.objects.all()

    if current_user.role.name == '学生':
        # 如果登录者是个学生，筛选出他自己的成绩（学生不能看别的学生的成绩）
        student = Student.objects.get(user=current_user)
        grades = grades.filter(student=student)

    else:
        # 如果登录者是个老师，筛选出他执教的课程成绩
        teacher = Teacher.objects.get(user=current_user)
        grades = grades.filter(subject__teacher=teacher)


    if term:
        # 如果传入了学期，筛选出该学期的成绩
        grades = grades.filter(subject__term=term)

    if subject:
        # 如果传入了课程，筛选出该课程的成绩
        grades = grades.filter(subject=subject)

    return grades


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