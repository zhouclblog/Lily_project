from django.conf.urls import url
from lily_goods import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^list/(\d+)/$", views.goods_list, name="goods_list"),
    url(r"^detial/(\d+)/$", views.detial, name="goods_detial")

]
