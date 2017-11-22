# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now=True)),
                ('username', models.CharField(max_length=30, verbose_name='用户名')),
                ('password', models.CharField(max_length=30, verbose_name='密码')),
                ('email', models.CharField(max_length=40, verbose_name='邮箱')),
                ('is_activate', models.BooleanField(default=False, verbose_name='激活状态')),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
    ]
