import re
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from lily_user.models import UserInfo, Address
from django.http import HttpResponse,JsonResponse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO

from django.http import JsonResponse, HttpResponse
from Lily.settings import SECRET_KEY
from celery_tasks.tasks import send_active_email
from utils.decorators import login_required, require_GET
from django_redis import get_redis_connection


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
    yzm = request.POST.get('yzm')
    # 2.校验数据
    if not all([username, pwd, remember, yzm]):
        # 有数据为空
        return JsonResponse({'res':1})
    # 3.验证验证码
    yzm_str = request.session.get('verifycode')
    if yzm == yzm_str:
        # 验证码输入正确
        # 4.进行数据处理，查找对应的数据库信息
        passport = UserInfo.objects.get_one_passport(username=username, password=pwd)
        if passport:
            next_url = request.session.get('url_path', reverse('lily_goods:index'))
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
            request.session['passport_id'] = passport.id

            return jres
        else:
            # 用户名密码输入错误
            return JsonResponse({'res':0})

    else:
        # 验证码输入错误
        return JsonResponse({'res':3})

def logout(request):
    #　用户退出
    # 清空用户的session信息
    request.session.flush()
    # 跳转页面
    return redirect('#')

def verify_code(request):
    '''生成验证码'''
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    buf = BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

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


@login_required
def user_center_info(request):
    '''用户中心-信息页'''
    userinfo_id = request.session.get('userinfo_id')
    # 显示用户的信息
    username = UserInfo.objects.get_one_passport(userinfo_id=userinfo_id)
    addr = Address.objects.get_default_address(userinfo_id=userinfo_id)
    phone = Address.objects.filter(id=userinfo_id).recipient_phone
    email = UserInfo.objects.filter(id=userinfo_id).email
    # phone = request.GET.get('recipient_phone')
    # email = request.GET.get('email')

    # 显示用户中心页面
    return render(request, 'lily_user/contact.html', {'addr':addr,
                                                      'username':username,
                                                      "phone": phone,
                                                      "email":email,
                                                      'page':'user_center_info'})

@login_required
def user_order(request):
    '''用户中心-订单页'''

    return render(request, 'lily_user/dingdan.html',{'page':'user_order'})

@login_required
def user_address(request):
    '''用户中心-地址页'''
    userinfo_id = request.session.get('userinfo_id')

    if request.method == 'GET':
        addr = Address.objects.get_default_address(userinfo_id=userinfo_id)
        return render(request, 'lily_user/address.html', {'addr':addr, 'page':'user_address'})

    else:
        recipient_name = request.POST.get('username')
        recipient_addr = request.POST.get('addr')
        phone = request.POST.get('recipient_phone')

        if not all([recipient_name, recipient_addr, phone]):
            return render(request, 'lily_user/address.html', {'errmsg': '参数不能为空!'})

        Address.objects.add_one_address(userinfo_id=userinfo_id,
                                        recipient_name=recipient_name,
                                        recipient_addr=recipient_addr,
                                        recipient_phone=phone)

        return redirect(reverse('lily_user:user_address'))

@login_required
def address_handle(request):
    '''添加用户的收货地址'''

    recipient_name = request.POST.get('username')
    recipient_addr = request.POST.get('addr')
    phone = request.POST.get('phone')

    if not all([recipient_name, recipient_addr, phone]):
        return render(request, 'lily_user/address.html', {'errmsg': '参数不能为空!'})

    userinfo_id = request.session.get('userinfo_id')

    Address.objects.add_one_address(userinfo_id=userinfo_id,
                                    recipient_name=recipient_name,
                                    recipient_addr=recipient_addr,
                                    recipient_phone=phone)

    return redirect(reverse('lily_user:user_address'))






