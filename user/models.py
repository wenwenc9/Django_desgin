# orm文件，用于建立模型，之后可以通过django工具映射到数据库中
# 每个model是一个表，每个属性是一个字段，字段的verbose_name即为后台管理界面显示的名字
# CharFiled， IntegerFiled等对应mysql中相应的数据类型
from django.db import models
from datetime import datetime, timedelta
from pytz import timezone


class Role(models.Model):
    # 角色表
    name = models.CharField(max_length=20, verbose_name='角色名')
    desc = models.CharField(max_length=50, verbose_name='角色描述')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'


class TeacherValidationCode(models.Model):
    # 教师码表
    code = models.CharField(max_length=10, verbose_name='教师码')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    expire_days = models.IntegerField(default=7, verbose_name='有效天数')

    class Meta:
        verbose_name = '教师码'
        verbose_name_plural = '教师码'

    def get_expire_time(self):
        # 获取过期时间，也就是创建时间+有效天数
        return self.create_time + timedelta(days=self.expire_days)

    def get_now(self):
        # 获取当前时间（带时区，以便）
        now = datetime.now().replace(tzinfo=timezone('UTC'))
        return now

    def is_validate(self):
        # 确定是否有效，也就是比较现在时间是否大于过期时间
        return self.get_expire_time()>self.get_now()

    def __str__(self):
        return self.code


class PasswordQuestion(models.Model):
    # 密保问题表
    text = models.CharField(max_length=50, unique=True, verbose_name='密保问题文本')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = '密保问题'
        verbose_name_plural = '密保问题'


class User(models.Model):
    # 用户表
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=20, verbose_name='密码')
    # 角色，连接至角色表
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    # 密保问题，连接至密保问题表
    question = models.ForeignKey(PasswordQuestion, on_delete=models.CASCADE, verbose_name='密保问题')
    # 密保问题答案
    answer = models.CharField(max_length=30, verbose_name='密保问题答案')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


