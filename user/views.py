# 视图函数，处理用户请求的核心函数，与url对应
# 注意它们的装饰器，点进去可以看到装饰器的作用
# 分为两类，一种直接是一个函数，还有一种是一个类，这个类里边可以按照请求方式写不同的函数处理
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views import View
from .forms import LoginForm, RegisterForm, ModifyInfoForm, ModifyPasswordForm, GetPasswordForm
from .utils import authentic, add_user, login_required, check_username_unique, recoverPassword
from .parameters import *
from django.utils.decorators import method_decorator
from .captcha import Captcha
from io import BytesIO
from .models import PasswordQuestion


@login_required
def index(request, **kwargs):
    # 主页
    # 用户系统没有自己的主页，直接跳转到ems系统的主页
    # redirect: 重定向至另一个url
    # reverse: 根据url的名字获取url
    return redirect(reverse('ems:index'))


class LoginView(View):
    # 登录

    # get方法，直接渲染页面，传入error_message
    # render: 渲染一个html，context为传入html的参数
    def get(self, request, error_message=None):
        if not error_message:
            error_message = request.GET.get('error_message')
        if error_message:
            context = {
                'error_message': error_message
            }
        else:
            context = {}
        return render(request, 'user/login.html', context=context)

    # post方法，处理用户提交的登录信息，根据处理结果做不同的返回
    def post(self, request):
        form = LoginForm(request.POST)  # 将提交的数据先传入表单做个验证，参看表单
        if form.is_valid():
            # 通过表单验证，开始处理
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            captcha = form.cleaned_data['captcha']
            if captcha.lower() != request.session.get(CAPTCHA_TEXT):
                error_message = '验证码错误！'
                return self.get(request, error_message)
            authentication = authentic(username, password)  #验证用户名与密码
            if authentication['code'] == 200:
                # 验证通过，获取登录的user id， 存入session中，以便于后续使用
                user = authentication['data']['user']
                request.session[CURRENT_USER_ID] = user.id
                # 跳转到主页
                return redirect(reverse('user:index'))
            else:
                # 验证不通过，获取错误信息，返回get方法，传入error_message
                error_message= authentication['message']
                return self.get(request, error_message)
        else:
            # 未通过表单验证，从未通过的错误中取出一个，返回get方法，传入error_message
            error_message = form.errors.popitem()[1][0]
            return self.get(request, error_message=error_message)


class RegisterView(View):
    # 注册

    # get方法，直接渲染页面，传入error_message
    def get(self, request, error_message=None):
        questions = PasswordQuestion.objects.all()
        context = {
            'questions': questions
        }
        if error_message:
            context['error_message'] = error_message
        return render(request, 'user/register.html', context=context)

    # post方法，处理用户提交的注册信息，根据处理结果做不同的返回
    def post(self, request):
        form = RegisterForm(request.POST)  # 将提交的数据先传入表单做个验证，参看表单
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role_name = form.cleaned_data['role_name']
            question_text = form.cleaned_data['question_text']
            answer = form.cleaned_data['answer']
            teacher_code = form.cleaned_data['teacher_code']
            result = add_user(username, password, role_name, question_text, answer, teacher_code)  #添加用户
            if result['code'] == 200:
                # 成功，跳转到登录页面
                return redirect(reverse('user:login') + '?error_message=注册成功！')
            else:
                error_message= result['message']
                return self.get(request, error_message)
        else:
            error_message = form.errors.popitem()[1][0]
            return self.get(request, error_message=error_message)


@method_decorator(login_required, name='dispatch')
class ModifyView(View):
    # 修改信息

    # get方法，直接渲染页面，传入error_message
    # 注意这里的item参数，来自url，用来确定更改的信息类型
    # item为info：修改普通信息（用户名）
    # item为password：修改密码
    def get(self, request, item, error_message=None, **kwargs):
        if error_message:
            context = {
                'error_message': error_message
            }
        else:
            context = {}
        if item == 'info':
            return render(request, 'user/modifyInfo.html', context=context)
        elif item == 'password':
            return render(request, 'user/modifyPassword.html', context=context)

    # post方法，处理用户提交的修改信息，根据处理结果做不同的返回
    def post(self, request, item, **kwargs):
        current_user = kwargs.get(CURRENT_USER)  # 获取当前登录的用户，参看login_required
        error_message = None
        if item == 'info':
            # 修改用户名
            form = ModifyInfoForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                if check_username_unique(username):
                    # 检查是否已被占用
                    current_user.username = username
                    current_user.save()
                    error_message = '修改成功！'
                else:
                    error_message = '用户名已被占用！'
            else:
                error_message = form.errors.popitem()[1][0]
        elif item == 'password':
            # 修改密码
            form = ModifyPasswordForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['new_password']
                if current_user.password == old_password:
                    # 旧密码匹配，修改密码
                    current_user.password = new_password
                    current_user.save()
                    error_message = '修改成功！'
                else:
                    error_message = '原密码错误！'
            else:
                error_message = form.errors.popitem()[1][0]
        return self.get(request, item, error_message=error_message)


def logout(request, **kwargs):
    # 注销
    # 删除session中的用户id
    del request.session[CURRENT_USER_ID]
    # 跳转到登录页面
    return redirect(reverse('user:login'))


def graph_captcha(request, **kwargs):
    # 验证码生成
    # 通过Captcha生成一张验证码图片，输出为一个HttpResponse
    text,image = Captcha.gene_graph_captcha()
    # 将验证码存入session中
    request.session[CAPTCHA_TEXT] = text.lower()
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = HttpResponse(out.read())
    resp.content_type = 'image/png'
    return resp

class GetPasswordView(View):
    # 找回密码

    def get(self, request, error_message=None, **kwargs):
        questions = PasswordQuestion.objects.all()
        context = {
            'questions': questions
        }
        if error_message:
            context['error_message'] = error_message
        return render(request, 'user/getPassword.html', context=context)

    # post方法，处理用户提交的密保信息，根据处理结果做不同的返回
    def post(self, request, **kwargs):
        form = GetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            question_text = form.cleaned_data['question_text']
            answer = form.cleaned_data['answer']
            new_password = form.cleaned_data['new_password']
            # 修改密码，参看recoverPassword
            result = recoverPassword(username, question_text, answer, new_password)
            if result['code'] == 200:
                return redirect(reverse('user:login') + '?error_message=修改成功！')
            else:
                error_message = result['message']
                return self.get(request, error_message=error_message)
        else:
            error_message = form.errors.popitem()[1][0]
            return self.get(request, error_message=error_message)