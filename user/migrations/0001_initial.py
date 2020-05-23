# Generated by Django 2.2.4 on 2019-12-14 05:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('desc', models.CharField(max_length=50)),
                ('authority', models.IntegerField(default=1)),
                ('create_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('gender', models.IntegerField(choices=[(0, '未知'), (1, '男'), (-1, '女')], default=1)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Role')),
            ],
        ),
    ]