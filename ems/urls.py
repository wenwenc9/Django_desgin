from django.urls import path

from . import views

app_name = 'ems'
urlpatterns = [
    path('', views.index, name='index'),  # 主页
    path('relate/', views.RelateView.as_view(), name='relate'),  # 关联学号/工号
    path('grade/', views.grade_student, name='grade_student'),  # 成绩，学生
    path('grade/<int:subject_id>/', views.GradeTeacherView.as_view(), name='grade_teacher'),  # 成绩，老师
    path('subject/', views.subject, name='subject_teacher'),  # 课程选择
]