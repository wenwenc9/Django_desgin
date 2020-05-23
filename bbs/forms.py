from django.forms import Form, CharField


class ArticleForm(Form):
    # 文章验证表单
    title = CharField(required=True, max_length=30, error_messages={
        'required': '请输入标题！',
        'max_length': '输入的标题过长（超过30个字符）！',
    })
    content = CharField(required=True, error_messages={
        'required': '请输入一些内容！',
    })