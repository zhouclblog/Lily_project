# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('update_time', models.DateTimeField(verbose_name='修改时间', auto_now_add=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now=True)),
                ('recipient_name', models.CharField(verbose_name='收件人', max_length=20)),
                ('recipient_addr', models.CharField(verbose_name='收件地址', max_length=256)),
                ('recipient_phone', models.CharField(verbose_name='联系电话', max_length=11)),
                ('is_default', models.BooleanField(verbose_name='是否默认', default=False)),
            ],
            options={
                'db_table': 'address_info',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('update_time', models.DateTimeField(verbose_name='修改时间', auto_now_add=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now=True)),
                ('username', models.CharField(verbose_name='用户名', max_length=30)),
                ('password', models.CharField(verbose_name='密码', max_length=200)),
                ('email', models.CharField(verbose_name='邮箱', max_length=40)),
                ('is_activate', models.BooleanField(verbose_name='激活状态', default=False)),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='userinfo',
            field=models.ForeignKey(verbose_name='账户', to='lily_user.UserInfo'),
        ),
    ]
