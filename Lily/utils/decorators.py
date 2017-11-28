from django.shortcuts import redirect
from django.http import HttpResponse

def login_required(view_func):
	'''用户登陆判断装饰器'''
	def wrapper(request, *view_args, **view_kwargs):
		if request.session.has_key('islogin'):
			# 用户已登陆
			return view_func(request, *view_args, **view_kwargs)
		else:
			# 用户未登陆，跳转页面
			return redirect('#')
	return wrapper


def require_GET(view_func):
	'''请求方式装饰器'''
	def wrapper(request, *view_args, **view_kwargs):
		if request.method == 'GET':
			return view_func(request, *view_args, **view_kwargs)
		else:
			return HttpResponse('not allowed')
	return wrapper