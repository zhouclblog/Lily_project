from django.conf.urls import url
from lily_user import views

urlpatterns = [
    url(r"^register/$", views.register, name="register"),
    url(r"^register_handle/$", views.register_handle, name="register_handle"),

    url(r"^login/$", views.login, name="login"),# 显示登陆页面
    url(r"^login_check/$", views.login_check, name="login_check"),# 登陆校验
    url(r"^logout/$", views.logout, name="logout"),# 用户退出
    url(r"^verify_code/$", views.verify_code, name="verify_code"), # 生成验证码


    url(r"^check_user/$", views.check_user, name="check_user"),
    url(r"^email_active/$", views.email_active, name="email_active"),
    url(r"^active/$", views.active, name="active"),

    url(r'^user_center_info/$', views.user_center_info, name='user_center_info'),
    url(r'^user_order/$', views.user_order, name='user_order'),
    url(r'^user_address/$', views.user_address, name='user_address'),
    url(r'^address_handle/$', views.address_handle, name='address_handle'),

   


]
