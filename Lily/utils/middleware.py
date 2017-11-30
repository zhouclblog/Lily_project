class UrlPathRecordMiddleware(object):

    '''记录登陆之前访问的url'''
    EXCLUDE_URLS = ['/user/login/', '/user/logout/', '/user/register/', '/user/verify_code/']

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # 当用户请求的地址不在排除的列表中，同时不是ajax的get请求
        if request.path not in UrlPathRecordMiddleware.EXCLUDE_URLS and not request.is_ajax() and request.method == 'GET':
            request.session['url_path'] = request.path