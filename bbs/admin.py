from django.contrib import admin
from .models import Article, Comment

# 在后台管理界面中注册模型，需要在后台管理界面中显示的模型都要这样注册一下
admin.site.register(Article)
admin.site.register(Comment)
