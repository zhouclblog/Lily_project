from django.shortcuts import render
from django.http import JsonResponse
from lily_goods.models import GoodsInfo
from utils.decorators import login_required
from django_redis import get_redis_connection
# Create your views here.

@login_required
def show_cart(request):
    '''显示购物车页面'''
    passport_id = request.session.get('passport_id')
    # 链接redis数据库，查询商品的数据
    conn = get_redis_connection('default')
    cart_key = "cart_%d" % passport_id
    # hgetall返回的是一个字典
    goods_dict = conn.hgetall(cart_key)
    goods_li = []

    # 计算商品的总价格和总数量
    total_price = 0
    total_count = 0

    for goods_id, goods_count in goods_dict.items():
        # 根据商品id查找商品信息
        goods = GoodsInfo.objects.get_good_by_id(goods_id=goods_id)
        goods.count = goods_count
        goods.amount = int(goods_count)*goods.goods_price_now
        goods_li.append(goods)

        total_count += int(goods_count)
        total_price += int(goods_count)*goods.goods_price_now

    # 定义模板上下文
    context = {'goods_li':goods_li, 'total_count':total_count,
               'total_price':total_price}


    return render(request, 'lily_cart/cart.html', context)

def cart_add(request):
    '''向购物车中添加数据'''
    # 判断用户是否登陆
    if not request.session.has_key('islogin'):
        return JsonResponse({'res':0, 'errmsg':'请先登陆'})

    # 接收数据，接收端发来的数据，商品id，商品数量
    goods_id = request.POST.get('goods_id')
    goods_count = request.POST.get('goods_count')
    # print(goods_id)
    # 校验数据
    if not all ([goods_id, goods_count]):
        return JsonResponse({'res':1, 'errmsg':'数据不完整'})

    # 根据商品id，查找对应商品信息
    goods = GoodsInfo.objects.get_good_by_id(goods_id=goods_id)
    if goods is None:
        return JsonResponse({'res':2, 'errmsg':'商品不存在'})
    try:
        count = int(goods_count)
    except Exception as e:
        return JsonResponse({'res':3, 'errmsg':'商品数目不合法'})

    # 添加商品数据到购物车，使用redis数据库
    # 每个用户的购物车创建一条hash数据，cart_用户id:商品id　商品数量
    conn = get_redis_connection('default')
    passport_id = request.session.get('passport_id')
    # print(passport_id)
    cart_key = "cart_%d" % passport_id
    # print(cart_key)
    # 根据cart_key和passport_id来查找对应商品的数量
    res_count = conn.hget(cart_key, goods_id)
    if res_count is None:
        # 如果商品数量为空，代表用户购物车中没有该商品，则添加
        res_count = count
    else:
        # 不为空，代表用户购物车中存在该商品，则追加商品数量
        res_count = int(res_count) + count
    # print(res_count)
    # 判断商品的库存
    if res_count > goods.goods_stock:
        return JsonResponse({'res':4, 'errmsg':'商品库存不足'})
    else:
        conn.hset(cart_key, goods_id, res_count)
        return JsonResponse({'res':5})

def cart_count(request):
    '''查询购物车商品数量'''
    # 判断用户是否登陆
    if not request.session.get('islogin'):
        return JsonResponse({'res':0, 'errmsg':'请先登陆'})

    # 链接redis数据库，计算所有商品的商品数量    
    conn = get_redis_connection('default')
    passport_id = request.session.get('passport_id')
    cart_key = "cart_%d" % passport_id
    # print(cart_key)
    # 获取用户所有的商品数量
    res = 0
    res_list = conn.hvals(cart_key)
    # print(res_list)
    # 遍历获取到的每件商品商品数量进行累加
    for i in res_list:
        print(i)
        res += int(i)
    # print(res)
    # print(passport_id)
    # 返回商品总量
    return JsonResponse({'res':res})


def cart_update(request):
    '''更新购物车的商品数量'''
    # 判断用户是否登陆
    if not request.session.has_key('islogin'):
        return JsonResponse({'res':0, 'errmsg':'请先登陆'})

    # 接收数据
    goods_id = request.POST.get('goods_id')
    goods_count = request.POST.get('goods_count')

    # 校验数据
    if not all([goods_id, goods_count]):
        return JsonResponse({'res':1, 'errmsg':'数据不完整'})

    # 根据商品id查找对应商品
    goods = GoodsInfo.objects.get_good_by_id(goods_id=goods_id)
    if goods is None:
        return JsonResponse({'res':2, 'errmsg':'商品不存在'})

    try:
        goods_count = int(goods_count)
    except Exception as e:
        return JsonResponse({'res':3, 'errmsg':'商品数量不是数字'})

    # 链接redis数据库
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % request.session.get('passport_id')

    # 判断商品库存
    if goods_count > goods.goods_stock:
        return JsonResponse({'res':4, 'errmsg':'商品库存不足'})

    # 更新购物车的数据
    conn.hset(cart_key, goods_id, goods_count)
    return JsonResponse({'res':5})


def cart_del(request):
    '''删除购物车的数量'''
    # 判断用户是否登陆
    if not request.session.has_key('islogin'):
        return JsonResponse({'res':0, 'errmsg':'请先登陆'})

    # 接收数据
    goods_id = request.POST.get('goods_id')
    
    # 数据校验
    if not all([goods_id]):
        return JsonResponse({'res':1, 'errmsg':'数据不完整'})

    # 根据商品id查找商品
    goods = GoodsInfo.objects.get_good_by_id(goods_id=goods_id)

    if goods is None:
        return JsonResponse({'res':2,'errmsg':'商品不存在'})

    # 链接redis数据库
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % request.session.get('passport_id')

    # 删除数据库中的数据
    conn.hdel(cart_key, goods_id)

    return JsonResponse({'res':3})

