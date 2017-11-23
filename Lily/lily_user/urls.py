from django.conf.urls import url
from lily_user import views

urlpatterns = [
    url(r"^register/$", views.register, name="register"),
    url(r"^register_handle/$", views.register_handle, name="register_handle"),
    url(r"^check_user/$", views.check_user, name="check_user"),
    url(r"^email_active/$", views.email_active, name="email_active"),
    url(r"^active/$", views.active, name="active"),
]
