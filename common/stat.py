"""程序逻辑中的状态码"""

OK = 0  # 成功
VCODE_ERR = 1000  # 发送验证码失败
INVILD_VCODE = 1001  # 验证码无效
ACCESS_TOKEN_ERR = 1002  # 授权码接口错误
USER_INFO_ERR = 1003  # 用户信息接口错误
