from django.conf.urls import url
from lily_user import views

urlpatterns = [
    url(r"^register/$", views.register, name="register"),
    url(r"^register_handle/$", views.register_handle, name="register_handle"),
<<<<<<< HEAD
    url(r"^check_user/$", views.check_user, name="check_user"),
    url(r"^email_active/$", views.email_active, name="email_active"),
    url(r"^active/$", views.active, name="active"),
=======
    url(r"^login/$", views.login, name="login"),
    url(r"^login_check/$", views.login_check, name="login_check"),
    url(r"^logout/$", views.logout, name="logout"),


>>>>>>> b94bad52feb2bb1c00498f81e35f602d1dc16c2e
]
