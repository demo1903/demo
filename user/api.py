from django.http import JsonResponse
from django.core.cache import cache

from common import keys
from user import logics
from common import stat
from user.models import User


def get_vcode(request):
    """获取短信验证码"""
    phonenum = request.GET.get('phonenum')

    # 发送验证码,并检查是否发送成功
    if logics.send_vcode(phonenum):
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})


def check_vcode(request):
    """进行验证,并且登录或者注册"""
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    cached_vcode = cache.get(keys.VCODE_KEY.format(phonenum))  # 从缓存中取出验证码
    # 判断vcode和cached_vcode是否为空,且是否相等
    if vcode and cached_vcode and vcode == cached_vcode:
        # 取出用户
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            # 如果用户不存在,直接创建出来
            user = User.objects.create(
                phonenum=phonenum,
                nickname=phonenum,
            )
        request.session['uid'] = user.id
        return JsonResponse({'code': stat.OK, 'data':user.to_dict()})
    else:
        return JsonResponse({'code': stat.INVILD_VCODE, 'data': None})
