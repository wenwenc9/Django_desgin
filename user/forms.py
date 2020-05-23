# 表单文件，接收用户从前端界面发送过来的数据，验证数据的有效性
# 每个验证表单都包含一些字段，每个字段包含一些验证器
# 注意这里的字段名必须与前端传入的input的name属性一致
from django.forms import Form, CharField, ValidationError


class LoginForm(Form):
    # 登录信息验证表单
    # 用户名验证（长度，输入必要性）
    # 注意error_message是自定义的验证错误信息，
    # error_message是一个dict，key为验证器的名称， value为对应的验证器验证失败时的信息
    # 注意这里的max_length要与数据库中max_length相匹配，以免出现数据库中的最大存储长度
    # 只有10位，验证通过的数据却有20位这种情况
    username = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的用户名过长（超过20个字符）！',
        'required': '请输入用户名！',
    })
    # 密码验证（长度，输入必要性）
    password = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的密码过长（超过20个字符）！',
        'required': '请输入密码！',
    })
    captcha = CharField(max_length=4, required=True, error_messages={
        'max_length': '验证码错误！',
        'required': '请输入验证码！',
    })


class RegisterForm(Form):
    # 注册信息验证表单
    # 用户名验证（长度，输入必要性）
    username = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的用户名过长（超过20个字符）！',
        'required': '请输入用户名！',
    })
    # 密码验证（长度，输入必要性）
    password = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的密码过长（超过20个字符）！',
        'required': '请输入密码！',
    })
    # 重复输入密码验证（长度，输入必要性）
    repeat_password = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的密码过长（超过20个字符）！',
        'required': '请再次输入密码！',
    })
    # 角色验证（输入必要性）
    role_name = CharField(required=True, error_messages={
        'required': '请选择角色！',
    })
    # 密保问题（输入必要性）
    question_text = CharField(required=True, error_messages={
        'required': '请选择密保问题！',
    })
    # 密保问题答案（输入必要性）
    answer = CharField(max_length=30, required=True, error_messages={
        'max_length': '输入的答案过长（超过30个字符）！',
        'required': '请输入密保问题答案！',
    })
    # 教师码验证（长度）
    teacher_code = CharField(max_length=10, required=False, error_messages={
        'max_length': '输入的教师码过长（超过10个字符）！',
    })

    # 自定义验证器
    # 对于某些字段，简单的长度等基本验证不能满足需求，可以自定义验证器进行验证
    # 函数名必须形如 clean_XXX (XXX即为要验证的字段名，必须与上边定义的名称一致)
    # 只能验证已经定义过的字段，也就是说哪怕你不需要基本验证，也一定要先在上边定义一下名字
    # 验证失败：raise ValidationError(error_message)
    # 验证成功：返回字段名（必须返回，不可省略）
    def clean_repeat_password(self):
        # 这里需要验证一下用户输入的密码与重复确认的密码是否一致
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        if repeat_password != password:
            raise ValidationError('两次输入的密码不一致！')
        else:
            return repeat_password

    def clean_teacher_code(self):
        # 这里是验证角色为教师时是否输入了教师码，未输入则验证失败
        # 注意并没有限定角色是学生时不可以输入教师码，反正传到后台也不会用到
        teacher_code = self.cleaned_data['teacher_code'].replace(' ', '')
        role_name = self.cleaned_data['role_name']
        if role_name == '教师' and len(teacher_code)==0 :
            raise ValidationError('请输入教师码或更改注册角色！')
        else:
            return teacher_code


class ModifyInfoForm(Form):
    # 修改信息表单验证
    # 目前只有用户名可以改
    username = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的用户名过长（超过20个字符）！',
        'required': '请输入用户名！',
    })


class ModifyPasswordForm(Form):
    # 修改密码表单验证
    old_password = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的密码过长（超过20个字符）！',
        'required': '请输入旧密码！',
    })
    new_password = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的密码过长（超过20个字符）！',
        'required': '请输入新密码！',
    })
    repeat_new_password = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的密码过长（超过20个字符）！',
        'required': '请再次输入新密码！',
    })

    def clean_repeat_new_password(self):
        # 这里验证两次输入的新密码
        # 注意不限制修改后的密码必须与旧密码不同，没有必要
        new_password = self.cleaned_data['new_password']
        repeat_new_password = self.cleaned_data['repeat_new_password']
        if repeat_new_password != new_password:
            raise ValidationError('两次输入的密码不一致！')
        else:
            return repeat_new_password


class GetPasswordForm(Form):
    # 找回密码表单验证

    username = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的用户名过长（超过20个字符）！',
        'required': '请输入用户名！',
    })
    # 密保问题（输入必要性）
    question_text = CharField(required=True, error_messages={
        'required': '请选择密保问题！',
    })
    # 密保问题答案（输入必要性）
    answer = CharField(max_length=30, required=True, error_messages={
        'max_length': '输入的答案过长（超过30个字符）！',
        'required': '请输入密保问题答案！',
    })
    new_password = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的密码过长（超过20个字符）！',
        'required': '请输入新密码！',
    })
    repeat_new_password = CharField(max_length=20, required=True, error_messages={
        'max_length': '输入的密码过长（超过20个字符）！',
        'required': '请再次输入新密码！',
    })

    def clean_repeat_new_password(self):
        # 这里验证两次输入的新密码
        # 注意不限制修改后的密码必须与旧密码不同，没有必要
        new_password = self.cleaned_data['new_password']
        repeat_new_password = self.cleaned_data['repeat_new_password']
        if repeat_new_password != new_password:
            raise ValidationError('两次输入的密码不一致！')
        else:
            return repeat_new_password
