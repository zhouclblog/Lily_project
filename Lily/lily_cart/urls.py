from django.conf.urls import url
from lily_cart import views

urlpatterns = [
   url(r"^show/", views.show_cart, name="show_cart"), # 显示购物车页面
   url(r"^add/", views.cart_add, name="cart_add"), # 向购物车中添加数据
   url(r"^count/", views.cart_count, name="cart_count"), # 查询购物车中的商品数量
   url(r"^update/", views.cart_update, name="cart_update"), # 更新购物车中的商品数量
   url(r"^del/", views.cart_del, name="cart_del"), # 删除购物车中的商品数量

]
