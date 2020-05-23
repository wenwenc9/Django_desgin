# 设置url路径
# 也就是设置网页访问url时对应的处理函数
# 详情可以点进函数里边去看
from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),  # 用户主页
    path('login/', views.LoginView.as_view(), name='login'),  # 登录
    path('register/', views.RegisterView.as_view(), name='register'),  # 注册
    path('modify/<str:item>', views.ModifyView.as_view(), name='modify'),  # 修改信息或密码
    path('logout/', views.logout, name='logout'),  # 注销
    path('captcha/', views.graph_captcha, name='captcha'),  # 验证码
    path('getpassword/', views.GetPasswordView.as_view(), name='getPassword'),  # 验证码
]



