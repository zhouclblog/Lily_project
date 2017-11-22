from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import re
from lily_user.models import UserInfo
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Create your views here.
def register(request):
    # 用来显示注册页面
    return render(request, "lily_user/register.html")


def register_handle(request):
    # 用来处理用户注册信息
    username = request.PORT.get("username")
    phone_num = request.PORT.get("phone_num")
    email = request.PORT.get("email")
    password = request.PORT.get("password")

    if not all([username, phone_num, email, password]):
        redirect(reverse("lily_user:register"))

    # 5-20位字母、数字或下划线组合，首字符必须为字母。
    if not re.match(r"[a-zA-Z][a-zA-Z0-9_]{5,20}", username):
        render(request, "lily_user/register.html", {"error": "用户名必须5-20位字母、数字或下划线组合，首字符必须为字母"})

    if not re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}", password):
        render(request, "lily_user/register.html", {"error": "密码必须包含大小写字母和数字的组合，不能使用特殊字符，长度在8-10之间"})

    if not re.match(r"(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}", phone_num):
        render(request, "lily_user/register.html", {"error": "手机号码输入不合法"})

    if not re.match(r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*", email):
        render(request, "lily_user/register.html", {"error": "邮箱地址不符合要求"})

    user_info = UserInfo.objects.add_one_message(username, password, email)

    return redirect(reverse("lily_user:login"))



