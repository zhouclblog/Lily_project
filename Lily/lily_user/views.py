import re
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from lily_user.models import UserInfo
from django.http import HttpResponse,JsonResponse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.http import JsonResponse, HttpResponse
from Lily.settings import SECRET_KEY
from celery_tasks.tasks import send_active_email

# Create your views here.
def register(request):
    # 用来显示注册页面
    return render(request, "lily_user/register.html")


def register_handle(request):
    # 用来处理用户注册信息
    username = request.POST.get("username")
    phone_num = request.POST.get("phone_num")
    email = request.POST.get("email")
    password = request.POST.get("password")

    if not all([username, phone_num, email, password]): 
        redirect(reverse("lily_user:register"))

    # 5-20位字母、数字或下划线组合，首字符必须为字母。
    if not re.match(r"[a-zA-Z][a-zA-Z0-9_]{5,20}", username):
        return render(request, "lily_user/register.html", {"error": "用户名必须5-20位字母、数字或下划线组合，首字符必须为字母"})

    if not re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}", password):
        return render(request, "lily_user/register.html", {"error": "密码必须包含大小写字母和数字的组合，不能使用特殊字符，长度在8-16之间"})

    if not re.match(r"(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}", phone_num):
        return render(request, "lily_user/register.html", {"error": "手机号码输入不合法"})

    if not re.match(r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*", email):
        return render(request, "lily_user/register.html", {"error": "邮箱地址不符合要求"})

    user_info = UserInfo.objects.add_one_message(username, password, email)

    return redirect(reverse("lily_user:login"))

def login(request):
    # 显示登陆页面
    # 判断是否有键名为username的cookie
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        checked = 'checked'
    else:
        username = ""
        checked = ""
    return render(request, "lily_user/login.html", {'username':username, 'checked':checked})

def login_check(request):
    # 登陆校验
    # 1.接收数据
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')
    remember = request.POST.get('remember')
    # 2.校验数据
    if not all([username, pwd, remember]):
        # 有数据为空
        return JsonResponse({'res':1})
    # 3.进行数据处理，查找对应的数据库信息
    passport = UserInfo.objects.get_one_passport(username=username, password=pwd)
    if passport:
        next_url = request.session.get('url_path', '#')
        jres = JsonResponse({'res':2, 'next_url':next_url})
        # 判断是否记住用户名
        if remember == 'true':
            # 记住用户名
            jres.set_cookie('username', username, max_age=7*24*3600)
        else:
            # 不记住用户名
            jres.delete_cookie('username')
        # 用户名密码输入正确,记录登陆状态
        request.session['islogin'] = True
        request.session['username'] = username

        return jres
    else:
        # 用户名密码输入错误
        return JsonResponse({'res':0})

def logout(request):
    #　用户退出
    # 清空用户的session信息
    request.session.flush()
    # 跳转页面
    return redirect('#')




def check_user(request):
    username = request.GET.get("username")

    if not username:
        return JsonResponse({"res": 1})

    try:
        UserInfo.objects.get(username=username)
    except:
        return JsonResponse({"res": 2})

    return JsonResponse({"res": 0})

def email_active(request):
    username = request.GET.get("username")
    email = request.GET.get("email")

    if not username:
        return JsonResponse({"res": 1})

    serializer = Serializer(SECRET_KEY, 3600)

    token = serializer.dumps({"confirm": username}).decode()
    send_active_email(token, email, username)
    return JsonResponse({"res": 0})


def active(request):
    token = request.GET.get("token")
    try:
        serializer = Serializer(SECRET_KEY, 3600)
        info = serializer.loads(token)
        username = info["confirm"]

        user_info = UserInfo.objects.get(username=username)
        user_info.is_activate = True
        user_info.save()
        return redirect(reverse("lily_user:login"))

    except:
        return HttpResponse("激活链接已过期")

