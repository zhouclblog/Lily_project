from django.shortcuts import redirect

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