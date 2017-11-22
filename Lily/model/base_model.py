# -*- coding: utf-8 -*-

from django.db import models

class BaseModel(models.Model):

    is_delete = models.BooleanField(default=False, verbose_name="删除标记")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    class Meta(object):

        abstract = True
