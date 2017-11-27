# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lily_goods', '0003_auto_20171126_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodstype',
            name='type_belong',
            field=models.SmallIntegerField(choices=[(0, '春暖花开'), (1, '清凉一夏'), (2, '秋风飒爽'), (3, '暖冬时尚'), (4, '温暖贴心'), (5, '职场英姿'), (6, '更多种类')], default=0, verbose_name='各商品种类所属季节'),
            preserve_default=False,
        ),
    ]
