# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsImages',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('image_name', models.CharField(verbose_name='图片名称', max_length=60)),
            ],
            options={
                'db_table': 'goods_image',
            },
        ),
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('goods_id', models.CharField(verbose_name='商品id', primary_key=True, max_length=20, serialize=False)),
                ('goods_name', models.CharField(verbose_name='商品名称', max_length=200)),
                ('goods_stock', models.IntegerField(verbose_name='库存')),
                ('goods_sales', models.IntegerField(verbose_name='销量')),
                ('comment_num', models.IntegerField(verbose_name='评论数量')),
                ('good_comment', models.IntegerField(verbose_name='好评数量')),
                ('middle_comment', models.IntegerField(verbose_name='中评数量')),
                ('bad_comment', models.IntegerField(verbose_name='差评数量')),
                ('goods_ori_price', models.DecimalField(verbose_name='商品原价', max_digits=10, decimal_places=2)),
                ('goods_price', models.DecimalField(verbose_name='商品价格', max_digits=10, decimal_places=2)),
                
                ('goods_ad', models.CharField(verbose_name='商品的广告信息', max_length=400)),
            ],
            options={
                'db_table': 'goods_info',
            },
        ),
        migrations.CreateModel(
            name='GoodsShop',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('shop_name', models.CharField(verbose_name='商店名称', max_length=40)),
            ],
            options={
                'db_table': 'goods_shop',
            },
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('update_time', models.DateTimeField(auto_now_add=True, verbose_name='修改时间')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('type_name', models.CharField(verbose_name='商品种类', max_length=20)),
            ],
            options={
                'db_table': 'goods_type',
            },
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='goods_shop',
            field=models.ForeignKey(verbose_name='标记商品商店', to='lily_goods.GoodsShop'),
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='goods_type',
            field=models.ForeignKey(verbose_name='标记商品种类', to='lily_goods.GoodsType'),
        ),
        migrations.AddField(
            model_name='goodsimages',
            name='goods_id',
            field=models.ForeignKey(verbose_name='商品id', to='lily_goods.GoodsInfo'),
        ),
    ]
