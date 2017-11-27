# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lily_goods', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodsinfo',
            old_name='goods_ori_price',
            new_name='goods_price_ori',
        ),
    ]
