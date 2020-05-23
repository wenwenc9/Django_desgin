from django.contrib import admin
from .models import Role, User, TeacherValidationCode, PasswordQuestion

# 在后台管理界面中注册模型，需要在后台管理界面中显示的模型都要这样注册一下
admin.site.register(Role)
admin.site.register(User)
admin.site.register(TeacherValidationCode)
admin.site.register(PasswordQuestion)