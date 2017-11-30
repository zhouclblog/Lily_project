from django.db import models
from model.base_model import BaseModel
from django.db.models import Q

# Create your models here.
class GoodsInfoManager(models.Manager):
    def get_goods_info(self, factor):
        # 通过传入的条件进行排序获得查寻集并返回
        goods_info = self.exclude(goodsimages__image_name="no image").order_by("-%s" % factor)

        return goods_info

    def get_goods_by_sort(self, type_id=None, sort="default"):

        if sort == "default":
            goods_info = self.filter(Q(goods_type=type_id) & (~Q(goodsimages__image_name="no image")))
        elif sort == "hot":
            goods_info = self.filter(Q(goods_type=type_id) & (~Q(goodsimages__image_name="no image"))).order_by("-goods_sales")
        elif sort == "good":
            goods_info = self.filter(Q(goods_type=type_id) & (~Q(goodsimages__image_name="no image"))).order_by("-good_comment")
        elif sort == "price":
            goods_info = self.filter(Q(goods_type=type_id) & (~Q(goodsimages__image_name="no image"))).order_by("goods_price_now")

        return goods_info

    def get_good_by_id(self, goods_id):
        # 根据商品id查找商品信息
        try:
            goods = self.get(goods_id=goods_id)
        except self.model.DoesNotExist:
            # 不存在商品信息
            goods = None
        return goods

class GoodsTypeManager(models.Manager):
    pass

class GoodsShopManager(models.Manager):
    pass

class GoodsImagesManager(models.Manager):
    pass



class GoodsInfo(BaseModel):
    objects = GoodsInfoManager()

    goods_id = models.CharField(max_length=20, primary_key=True, verbose_name="商品id")
    goods_type = models.ForeignKey("GoodsType", verbose_name="标记商品种类")
    goods_name = models.CharField(max_length=200, verbose_name="商品名称")
    goods_shop = models.ForeignKey("GoodsShop", verbose_name="标记商品商店")
    # 库存统一设为2000
    goods_stock = models.IntegerField(verbose_name="库存")
    # 销量取评论总数
    goods_sales = models.IntegerField(verbose_name="销量")
    comment_num = models.IntegerField(verbose_name="评论数量")
    good_comment = models.IntegerField(verbose_name="好评数量")
    middle_comment = models.IntegerField(verbose_name="中评数量")
    bad_comment = models.IntegerField(verbose_name="差评数量")
    
    goods_price_now = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品原价')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    goods_ad = models.CharField(max_length=400, verbose_name="商品的广告信息")

    class Meta(object):
        db_table = "goods_info"


class GoodsType(BaseModel):
    belong_choice = (
                        (0, "春暖花开"),
                        (1, "清凉一夏"),
                        (2, "秋风飒爽"),
                        (3, "暖冬时尚"),
                        (4, "温暖贴心"),
                        (5, "职场英姿"),
                        (6, "更多种类"),
    )
    objects = GoodsTypeManager()
    type_name = models.CharField(max_length=20, verbose_name="商品种类")
    type_belong = models.SmallIntegerField(choices=belong_choice, verbose_name="各商品种类所属季节")

    class Meta(object):
        db_table = "goods_type"


class GoodsShop(BaseModel):
    objects = GoodsShopManager()
    shop_name = models.CharField(max_length=40, verbose_name="商店名称")

    class Meta(object):
        db_table = "goods_shop"

class GoodsImages(BaseModel):
    objects = GoodsImagesManager()

    goods_id = models.ForeignKey("GoodsInfo", verbose_name="商品id")
    image_name = models.CharField(max_length=60, verbose_name="图片名称")

    class Meta(object):
        db_table = "goods_image"