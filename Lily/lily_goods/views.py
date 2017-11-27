from django.shortcuts import render
from lily_goods.models import GoodsInfo, GoodsShop, GoodsImages, GoodsType
from django.db.models import Sum
from django.core.paginator import Paginator

# Create your views here.

def index(request):

	# 用来保存所有要返回的模板上下文
	content = dict()

	# 按销量以及好评率取出前8名商家，取出各商家所属的总销量，
	# 以及商家中销量排名第一的商品图片作为封面
	res = GoodsInfo.objects.all().values_list("goods_shop_id").annotate(sales=Sum("goods_sales")).order_by("-sales")[1:9]
	goods_shop_li = list()
	for shop_id, amount in res:
		goods_shop = GoodsShop.objects.get(id=shop_id)
		goods_shop.amount = amount
		goods_shop_li.append(goods_shop)
	content["goods_shop"] = goods_shop_li
	# 取出销量排名前五的种类信息
	type_res = GoodsInfo.objects.all().values_list("goods_type_id").annotate(sales=Sum("goods_sales")).order_by("-sales")[1:6]

	goods_type_li = list()
	for type_id, amount in type_res:
		goods_type = GoodsType.objects.get(id=type_id)
		goods_type_li.append(goods_type)
	content["goods_type"] = goods_type_li
	# 将各种类放到页面上
	goods_belong_li = list()
	group_ids = GoodsType.belong_choice
	for group_id, name in group_ids:
		type_choice = GoodsType.objects.filter(type_belong=group_id)
		goods_belong_li.append((name, type_choice))
	content["types"] = goods_belong_li

	# 取出销量排名前六的商品信息
	goods_info = GoodsInfo.objects.get_goods_info("goods_sales")[0:6]
	for goods in goods_info:
		goods.image = "images/" + goods.goodsimages_set.get().image_name
	content["goods_hot"] = goods_info



	return render(request, "lily_goods/index.html", content)

def detial(request, goods_id):
	"""商品详细信息展示"""
	content = dict()

	goods_info = GoodsInfo.objects.get(goods_id=goods_id)

	content["goods_info"] = goods_info
	return render(request, "lily_goods/detial.html", content)


def shop(request):
	pass


def goods_list(request, type_id):
	"""商品分类信息展示页面"""
	sort = request.GET.get("sort")
	page = request.GET.get("page")

	if not sort:
		sort = "default"
	if not page:
		page = 1

	# 根据类别id获取当前分类
	try:
		goods_type = GoodsType.objects.get(id=type_id)
	except:
		return render(request, "404.html")
	content = dict()
	content["goods_type"] = goods_type
	# 根据分类信息查出所有商品，并进行排序
	goods_info = GoodsInfo.objects.get_goods_by_sort(type_id, sort)

	paginator = Paginator(goods_info, 60)
	goods_li = paginator.page(int(page))
	content["goods_li"] = goods_li

	page_num = paginator.num_pages

	if int(page_num) <=5:
		pages = range(1,page_num+1)
	elif int(page) <= 3:
		pages = range(1,6)
	elif page_num-int(page) < 2:
		pages = range(page_num-5, page_num+1)
	else:
		pages = range(int(page)-2, int(page)+3)
	content["pages"] = pages
	content["sort"] = sort
	content["type_id"] = type_id


	return render(request, "lily_goods/list.html", content)
