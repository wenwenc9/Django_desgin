from django.db import models
from user.models import User
from datetime import datetime


class Article(models.Model):
    # 文章表
    # 注意作者为某个user（而非student或teacher）
    title = models.CharField(max_length=30, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    publish_time = models.DateTimeField(default=datetime.now, verbose_name='发表时间')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'


class Comment(models.Model):
    # 文章表
    # 注意作者为某个user（而非student或teacher）
    article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)
    content = models.CharField(max_length=300, verbose_name='内容')
    publish_time = models.DateTimeField(default=datetime.now, verbose_name='发表时间')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'