from django.forms import Form, CharField, IntegerField


class RelateForm(Form):
    # 关联验证表单
    id = IntegerField(required=True, error_messages={
        'required': '请输入学号或工号！',
    })
    password = CharField(max_length=10, required=True, error_messages={
        'max_length': '输入的校园卡密码过长（超过10个字符）！',
        'required': '请输入校园卡密码！',
    })
