from django.core.cache import cache
from django.shortcuts import redirect

from common import keys
from user import logics
from common import stat
from libs.http import render_json
from swiper import cfg
from user.models import User
from user.forms import UserForm, ProfileForm


def get_vcode(request):
    """获取短信验证码"""
    phonenum = request.GET.get('phonenum')

    # 发送验证码,并检查是否发送成功
    if logics.send_vcode(phonenum):
        return render_json()
    else:
        return render_json(code=stat.VCODE_ERR)


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
        # 使用session记录登录状态
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=stat.INVILD_VCODE)


def wb_auth(request):
    # 用户授权页
    return redirect(cfg.WB_AUTH_URL)


def wb_callback(request):
    # 微博回调接口
    code = request.GET.get('code')
    # 获取授权令牌
    access_token, wb_uid = logics.get_access_token(code)
    if not access_token:
        return render_json(code=stat.ACCESS_TOKEN_ERR)

    # 获取用户信息
    user_info = logics.get_user_info(access_token, wb_uid)
    if not user_info:
        return render_json(code=stat.USER_INFO_ERR)

    # 执行登录或者注册
    try:
        user = User.objects.get(phonenum=user_info['phonenum'])
    except User.DoesNotExist:
        # 如果用户不存在,直接创建出来
        # **user_info ---> 将字典进行一个拆包,把字典的每一个key作为一个参数返回进去
        user = User.objects.create(**user_info)
    request.session['uid'] = user.id
    return render_json(data=user.to_dict())


def get_profile(request):
    """获取个人资料"""
    profile_data = request.user.profile.to_dict()
    return render_json(data=profile_data)


def set_profile(request):
    """修改个人资料"""
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)

    # 检查User的数据
    if not user_form.is_valid():
        return render_json(code=stat.USER_DATA_ERR, data=user_form.errors)

    # 检查Profile的数据
    if not profile_form.is_valid():
        return render_json(code=stat.PROFILE_DATA_ERR, data=profile_form.errors)
    user = request.user
    # 保存用户的数据
    user.__dict__.update(user_form.cleaned_data)
    user.save()

    # 保存交友资料的数据
    user.profile.__dict__.update(profile_form.cleaned_data)
    user.profile.save()
    return render_json(code=stat.OK, data=None)


def upload_avatar(request):
    """上传个人形象"""
    avatar = request.FILES.get('avatar')
    logics.handle_avatar.delay(request.user, avatar)
    return render_json()
