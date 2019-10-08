from django.http import JsonResponse
from user import logics


def get_vcode(request):
    """获取短信验证码"""
    phonenum = request.GET.get('phonenum')

    # 发送验证码,并检查是否发送成功
    if logics.send_vcode(phonenum):
        return JsonResponse({'code': 0, 'data': None})
    else:
        return JsonResponse({'code': 1000, 'data': None})


def check_vcode(request):
    """进行验证,并且登录或者注册"""
    pass
