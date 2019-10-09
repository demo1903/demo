"""程序逻辑配置和第三方平台配置"""
from urllib.parse import urlencode

"""云之讯配置"""
YZX_API = 'https://open.ucpaas.com/ol/sms/sendsms'
YZX_ARGS = {
    "sid": "5450062e93d0c03fc1575cda146bea91",
    "token": "36864962f3561dd15ba46aacad1bdca4",
    "appid": "48a3062d2e8145029574fb115b55e2e9",
    "templateid": "506880",
    "param": None,
    "mobile": None,
}

"""微博配置"""
WB_APP_KEY = '3888486497'
WB_APP_SECRET = 'e42cffa2087df4f6b700ae28ec8019d6'
WB_CALLBACK = 'http://127.0.0.1:8000/weibo/wb_callback'

# 第一步:authorize 授权接口
WB_AUTH_API = 'https://api.weibo.com/oauth2/authorize'
WB_AUTH_ARGS = {
    'client_id': WB_APP_KEY,
    'redirect_uri': WB_CALLBACK,
    'display': 'default',
}
WB_AUTH_URL = '{}?{}'.format(WB_AUTH_API, urlencode(WB_AUTH_ARGS))

# 第二步:AccessToken 接口
WB_ACCESS_TOKEN_API = 'https://api.weibo.com/oauth2/access_token'
WB_ACCESS_TOKEN_ARGS = {
    'client_id': WB_APP_KEY,
    'client_secret': WB_APP_SECRET,
    'grant_type': 'authorization_code',
    'redirect_uri': WB_CALLBACK,
    'code': None,
}

# 第三部:获取用户信息
WB_USER_SHOW_API = 'https://api.weibo.com/2/users/show.json'
WB_USER_SHOW_ARGS = {
    'access_token': None,
    'uid': None,
}
