# Generated by Django 2.2.4 on 2019-12-20 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20191220_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.PasswordQuestion', verbose_name='密保问题'),
        ),
    ]
