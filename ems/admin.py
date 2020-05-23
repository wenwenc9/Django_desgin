from django.contrib import admin
from .models import Student, Term, Teacher, Subject, Grade

# 在后台管理界面中注册模型，需要在后台管理界面中显示的模型都要这样注册一下
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Term)
admin.site.register(Subject)
admin.site.register(Grade)