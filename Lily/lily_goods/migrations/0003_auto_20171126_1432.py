# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lily_goods', '0002_auto_20171126_1406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodsinfo',
            old_name='goods_price_ori',
            new_name='goods_price_now',
        ),
    ]
