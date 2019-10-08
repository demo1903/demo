import random
import requests
from django.core.cache import cache

from swiper import cfg
from common import keys


def get_randcode(length: int) -> str:  # type hint写法
    """产生出指定长度的随机码"""
    chars = [str(random.randint(0, 9)) for i in range(length)]
    return ''.join(chars)


def send_vcode(phone):
    vcode = get_randcode(6)
    cache.set(keys.VCODE_KEY.format(phone), vcode, 180)  # 将验证码保存到缓存中,并设置过期时间
    print('验证码:', vcode)

    sms_args = cfg.YZX_ARGS.copy()
    sms_args['param'] = vcode
    sms_args['mobile'] = phone
    response = requests.post(cfg.YZX_API, json=sms_args)
    if response.status_code == 200:
        result = response.json()
        if result['code'] == '000000':
            return True
    return False
