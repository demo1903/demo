import requests
import random
from swiper import cfg


def get_randcode(length: int) -> str:  # type hint写法
    """产生出指定长度的随机码"""
    chars = [str(random.randint(0, 9)) for i in range(length)]
    return ''.join(chars)


def send_vcode(phone):
    vcode = get_randcode(5)
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


