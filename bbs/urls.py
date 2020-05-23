from django.urls import path

from . import views

app_name = 'bbs'
urlpatterns = [
    path('', views.index, name='index'), # 首页
    path('article/<int:page>/', views.article, name='article'),  # 文章列表
    path('publish', views.PublishView.as_view(), name='publish'),  # 发表文章
    path('detail/<int:id>/', views.detail, name='detail'),  # 文章详情
    path('comment/<int:id>/', views.comment, name='comment'),  # 发表评论
]