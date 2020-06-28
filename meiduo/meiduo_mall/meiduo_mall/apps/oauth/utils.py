from urllib.parse import urlencode, parse_qs
from django.conf import settings
from urllib.request import urlopen
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData

from .exceptions import QQAPIException
import logging
import json
from . import constants

logger = logging.getLogger('django')


class OAuthQQ(object):
    """QQ登录的工具类，封装了QQ登录的部分过程"""

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        """构造方法，用户初始化OAuthQQ对象， 并传入一些参数"""
        self.client_id = client_id or settings.QQ_CLIENT_ID
        self.client_secret = client_secret or settings.QQ_CLIENT_SECRET
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URI
        self.state = state or settings.QQ_STATE  # 用于保存登录成功后的跳转页面路径

    def get_qq_login_url(self):
        """提供QQ扫码登陆页面的url"""

        # 准备url
        login_url = 'https://graph.qq.com/oauth2.0/authorize?'

        # 准备参数
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
            'scope': 'get_user_info',
        }

        # url提供参数
        query_params = urlencode(params)

        # 拼接url
        login_url += query_params

        # 返回login_url
        return login_url

    def get_access_token(self, code):
        """
        获取access_token
        :param code: qq提供的code
        :return: access_token
        """
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        url = 'https://graph.qq.com/oauth2.0/token?'

        query_params = urlencode(params)
        url += query_params
        try:
            # 服务器向QQ服务器发送GET请求
            response = urlopen(url)

            # response响应对象用read()方法读取信息，得到bytes类型数据，bytes字符串用decode解码
            response_data = response.read().decode()

            # 用parse_qs将查询字符串准成字典
            data = parse_qs(response_data)

            # 读取access_token
            access_token = data.get('access_token')[0]
        except Exception as e:
            logger.error(e)
            # 在封装工具类时候，需要捕获异常，千万不要解决异常，谁调用谁解决
            raise QQAPIException('获取access_token失败')

        return access_token

    def get_openid(self, access_token):
        """
        获取用户的openid
        :param access_token: qq提供的access_token
        :return: open_id
        """
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token

        # 美多商城服务器向QQ服务器发起GET请求
        response_data = ''
        try:
            response = urlopen(url)
            response_data = response.read().decode()
            # 返回的数据 callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} )\n;
            data = json.loads(response_data[10:-4])
            openid = data.get('openid')

        except Exception as e:
            data = parse_qs(response_data)
            logger.error(e)
            raise QQAPIException('code=%s msg=%s' % (data.get('code'), data.get('msg')))

        return openid

    @staticmethod
    def generate_save_user_token(openid):
        """
        生成保存用户数据的token
        :param openid: 用户的openid
        :return: token
        """
        serializer = Serializer(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        data = {'openid': openid}
        token = serializer.dumps(data)
        return token.decode()

    @staticmethod
    def check_save_user_token(token):
        """
        检验保存用户数据的token
        :param token: token
        :return: openid or None
        """
        serializer = Serializer(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            return data.get('openid')
