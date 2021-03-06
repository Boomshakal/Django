"""
Django settings for ikahe project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd5av#d_$7p(ux9z_gwf^77=p$wssucdvl7mzlshlcuwa=0s$tv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'raven.contrib.django.raven_compat',  # sentry
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.sites',
    'django.contrib.staticfiles',
    'e_kanban.apps.EKanbanConfig',
    'users.apps.UsersConfig',
    'DjangoUeditor',  # Ueditor富文本编辑器
    # 'user_operation.apps.UserOperationConfig',
    'xadmin',
    'crispy_forms',  # xadmin必要插件
    'django_filters',
    'rest_framework',
    'corsheaders',  # 跨域请求
    'rest_framework.authtoken',  # TokenAuthentication
    'social_django',  # 第三方集成
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 跨域请求
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True  # 跨域请求

ROOT_URLCONF = 'ikahe.urls'

AUTH_USER_MODEL = 'users.UserProfile'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media").replace('\\', '/')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'ikahe.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ikahe',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '10.4.7.31',
        'PORT': '3306',
    },
    'OPTIONS': {
        "init_command": "SET storage_engine=INNODB;",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

REST_FRAMEWORK = {
    # docs
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',

    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    # 验证用户登录
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication', #全局配置认证
    ),

    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/day',
        'user': '100/day'
    }
}

# 设置要使用的第三方登录
AUTHENTICATION_BACKENDS = (
    # 用户验证
    'users.views.CustomBackend',

    'social_core.backends.github.GithubOAuth2',  # 使用GitHub登陆
    'social_core.backends.weibo.WeiboOAuth2',  # 使用微博登录
    'social_core.backends.weixin.WeixinOAuth2',  # 使用微信登录
    'social_core.backends.qq.QQOAuth2',  # 使用QQ登录
    'django.contrib.auth.backends.ModelBackend',  # 指定django的ModelBackend类
)

# 云片网 APIKEY
APIKEY = 'b3d3d8a162027e8cc0f21b65fd0452ab'

# 配置微博开放平台授权
# SOCIAL_AUTH_要使用登录模块的名称大小_KEY，其他如QQ相同
SOCIAL_AUTH_WEIBO_KEY = '1359594035'
SOCIAL_AUTH_WEIBO_SECRET = '7d33714722f4e5572c116ce2b2433a99'

SOCIAL_AUTH_GITHUB_KEY = '9b32c6c780ccfec10f0e'
SOCIAL_AUTH_GITHUB_SECRET = '3c7cdf5226c394d9d928d990aedbfe2c79876099'

SOCIAL_AUTH_WEIXIN_KEY = 'wx6d7e96f838ad657a'
SOCIAL_AUTH_WEIXIN_SECRET = '68aac1c3e3d904214e2d348f163a3411'

SOCIAL_AUTH_QQ_KEY = '101860365'
SOCIAL_AUTH_QQ_SECRET = 'a7fe8242ec8de112b9914303120d8426'

# 登录成功后跳转页面
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/home/'

# smtp 服务器地址
EMAIL_HOST = "smtp.163.com"
# 默认端口25，若请求超时可尝试465
EMAIL_PORT = 25
# 用户名
EMAIL_HOST_USER = "lihuiminqq@163.com"
# 邮箱代理授权码（不是邮箱密码）
EMAIL_HOST_PASSWORD = "Lhm922357"
# 是否使用了SSL 或者TLS（两者选其一）
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
# 发送人
EMAIL_FROM = "lihuiminqq@163.com"  #
# 默认显示的发送人，（邮箱地址必须与发送人一致），不设置的话django默认使用的webmaster@localhost
DEFAULT_FROM_EMAIL = "IKAHE<lihuiminqq@163.com>"

UEDITOR_SETTINGS = {
    "config": {
        "toolbars": [["source", "undo", "redo", "bold", "italic", "underline", "forecolor", "backcolor",
                      "superscript", "subscript", "justifyleft", "justifycenter", "justifyright", "insertorderedlist",
                      "insertunorderelist", "blockquote", "formatmatch", "removeformat", "autotypeset", "inserttable",
                      "pasteplain", "wordimage", "searchreplace", "map", "preview", "fullscreen"],
                     ["insertcode", "paragraph", "fontfamily", "fontsize", "link", "unlink", "simpleupload",
                      "insertvideo",
                      "attachment", "emotion", "date", "time"]]
    },
    'upload': {
        "imageUrlPrefix": "http://192.168.234.129:8000",  # 图片访问路径前缀
        "imagePathFormat": "/media/goods/upload/{yyyy}{mm}{dd}/{time}{rand:6}"
    },
}

# 配置django-redis缓存
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://:redis@192.168.234.129:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# drf-extensions 配置
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 30,
    'DEFAULT_CACHE_ERRORS': False,
}

# 支付宝配置
# private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private_2048.txt')
# ali_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_key_2048.txt')


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

import raven

RAVEN_CONFIG = {
    'dsn': '',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),

}
