from libs.http import render_json
from django.utils.deprecation import MiddlewareMixin

from common import stat
from user.models import User


class AuthorizeMiddleware(MiddlewareMixin):
    """登录验证中间件"""
    WHITE_LIST = [
        '/api/user/get_vcode',
        '/api/user/check_vcode',
        '/weibo/wb_auth',
        '/weibo/wb_callback',
    ]

    def process_request(self, request):
        if request.path in self.WHITE_LIST:
            return

        uid = request.session.get('uid')
        if not uid:
            return render_json(code=stat.LOGIN_REQUIRED.code)
        request.user = User.objects.get(id=uid)


class LogicErrMiddleware(MiddlewareMixin):
    """逻辑异常处理中间件"""

    def process_exception(self, request, exception):
        if isinstance(exception, stat.LogicErr):
            return render_json(code=exception.code, data=exception.data)
