# Generated by Django 2.2.4 on 2019-12-15 02:13

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20191215_0950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teachervalidationcode',
            name='expire_time',
        ),
        migrations.AddField(
            model_name='teachervalidationcode',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teachervalidationcode',
            name='expire_days',
            field=models.IntegerField(default=7, verbose_name='有效天数'),
        ),
        migrations.AlterField(
            model_name='role',
            name='authority',
            field=models.IntegerField(default=1, verbose_name='权限'),
        ),
        migrations.AlterField(
            model_name='role',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='role',
            name='desc',
            field=models.CharField(max_length=50, verbose_name='角色描述'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=20, verbose_name='角色名'),
        ),
        migrations.AlterField(
            model_name='teachervalidationcode',
            name='code',
            field=models.CharField(max_length=10, verbose_name='教师码'),
        ),
    ]
