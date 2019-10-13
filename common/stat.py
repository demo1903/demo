"""程序逻辑中的状态码"""
OK = 0     # 成功


class LogicErr(Exception):
    code = OK
    data = None

    def __init__(self, data=None):
        self.data = data or self.__class__.__name__


def gen_login_err(name, code):
    """生成一个逻辑异常类"""
    return type(name, (LogicErr,), {'code': code})


VCODE_ERR = gen_login_err('VCODE_ERR', 1000)                 # 发送验证码失败
INVILD_VCODE = gen_login_err('INVILD_VCODE', 1001)           # 验证码无效
ACCESS_TOKEN_ERR = gen_login_err('ACCESS_TOKEN_ERR', 1002)   # 授权码接口错误
USER_INFO_ERR = gen_login_err('USER_INFO_ERR', 1003)         # 用户信息接口错误
LOGIN_REQUIRED = gen_login_err('LOGIN_REQUIRED', 1004)       # 用户未登录
USER_DATA_ERR = gen_login_err('USER_DATA_ERR', 1005)         # 用户数据错误
PROFILE_DATA_ERR = gen_login_err('PROFILE_DATA_ERR', 1006)   # 用户交友资料数据错误
SwiperTypeErr = gen_login_err('SwiperTypeErr', 1007)                 # 滑动类型错误
SwipeRepeatErr = gen_login_err('SwipeRepeatErr', 1008)       # 重复滑动错误
