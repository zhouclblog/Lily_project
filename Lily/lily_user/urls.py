from django.conf.urls import url
from lily_user import views

urlpatterns = [
    url(r"^register/$", views.register, name="register"),
    url(r"^register_handle/$", views.register_handle, name="register_handle"),
    url(r"^login/$", views.login, name="login"),
    url(r"^login_check/$", views.login_check, name="login_check"),
    url(r"^logout/$", views.logout, name="logout"),


]
