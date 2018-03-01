"""
Django settings for d project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djandawgoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.conf.global_settings import DEFAULT_FILE_STORAGE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# import sys
# # 增加导包路径 , 一般把第0个""空出来
# sys.path.insert(1, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '15jeyophvs2h^b2qa5@eihbn1yv2zyjn5rr7#*g76y1y#%&slc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    # 安装应用
    #  django 用户认证系统规定,安装的应用名称需要和 'AUTH_USER_MODEL = 'users.User'' 单应用
    'users',
    'goods',
    'orders',
    'cart',
    'djcelery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 默认开启用户认证的中间件 , 用于用户认证, 包括用户是否的登陆
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 配置模板路径
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'd.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dalyfish',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': '127.0.0.1',  # 可以是远程数据库服务器,最好写ipv4地址
        'PORT': '3306'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

#  ********** 配置静态文件加载路径****************************************************************************
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    # 这句话的意思是默认去找static文件夹下的[和项目同名的=>booktest文件夹非必须]
    os.path.join(BASE_DIR, 'static')
]
#  ********** 配置静态文件加载路径 结束 ********************************************************************************
CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "localhost:6379",
        'TIMEOUT': 60,
    },
}
# 1.session 默认存储设置 存储到数据库
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# 2.session 存储在内存中
# SESSION_ENGINE='django.contrib.sessions.backends.cache'
# 3.可以将缓存和数据库同时使用：优先从本地缓存中获取，如果没有则从数据库中获取
# SESSION_ENGINE='django.contrib.sessions.backends.cached_db'
# 4.django-redis-sessions 存储到redis里 django-redis-sessions 配置 废弃！！！！！！！！！！
# SESSION_ENGINE = 'redis_sessions.session'
# SESSION_REDIS_HOST = 'localhost'
# SESSION_REDIS_PORT = 6379
# SESSION_REDIS_DB = 0
# SESSION_REDIS_PASSWORD = ''
# SESSION_REDIS_PREFIX = 'session'
# ##########废弃！！！！！！！！！！！！！！！！！！！！废弃！！！！！！！！！！
# 5 djnago-redis 的配置方式------------------------------------------------------------------------------------------
# 缓存
# Session
# http://django-redis-chs.readthedocs.io/zh_CN/latest/#session-backend
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/5",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 可以扩充
    # "mmdNewRedis": {
    #     "BACKEND": "django_redis.cache.RedisCache",
    #     "LOCATION": "redis://127.0.0.1:6379/5",
    #     "OPTIONS": {
    #         "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #     }
    # },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"  # 更换session引擎为缓存,默认存储在django_session表中
SESSION_CACHE_ALIAS = "default"  # default
# 5 djnago-redis 的配置方式 结束-------------------------------------------------------------------------------------

# ?????????????????????????????????????????  没有登陆情况下重定向的地址 ??????????????????????????????????????????
LOGIN_URL = '/users/login'
# ????????????????????????????????????????  没有登陆情况下重定向的地址结束 ???????????????????????????????????????
# 原因：在settings.py中设置AUTH_USER_MODEL时，编码规则为'应用.用户模型类'
#  AUTH_USER_MODEL = 'apps.users.User' 不符合规范 只能使用一个点,djang默认单应用
AUTH_USER_MODEL = 'users.User'
#
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 导入邮件模块
# EMAIL_HOST = 'smtp.yeah.net'  # 发邮件主机 smtp.yeah.net
# EMAIL_PORT = 25  # 发邮件端口 wofedmnlmegjcaca 25
# EMAIL_HOST_USER = 'dailyfreshzxc@yeah.net'  # 授权的邮箱 pxd7th@vip.qq.com
# EMAIL_HOST_PASSWORD = 'dailyfresh123'  # 邮箱授权时获得的密码，非注册登录密码
# EMAIL_FROM = '天天生鲜<dailyfreshzxc@yeah.net>'  # 发件人抬头 天天生鲜<pxd7th@vip.qq.com>

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 导入邮件模块
EMAIL_HOST = 'smtp.163.com'  # 发邮件主机 smtp.yeah.net
EMAIL_PORT = 25  # 发邮件端口 wofedmnlmegjcaca 25
EMAIL_HOST_USER = '15346566750@163.com'  # 授权的邮箱 pxd7th@vip.qq.com
EMAIL_HOST_PASSWORD = 'wy2921481'  # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = '天天生鲜<15346566750@163.com>'  # 发件人抬头 天天生鲜<pxd7th@vip.qq.com>

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 导入邮件模块
# EMAIL_HOST = 'smtp.qq.com'  # 发邮件主机 smtp.yeah.net
# EMAIL_PORT = 465  # 发邮件端口 wofedmnlmegjcaca 25
# EMAIL_HOST_USER = '453388937@qq.com'  # 授权的邮箱 pxd7th@vip.qq.com
# EMAIL_HOST_PASSWORD = 'xviwmcrwncyxbggh'  # 邮箱授权时获得的密码，非注册登录密码
# EMAIL_FROM = '天天生鲜<453388937@qq.com>'  # 发件人抬头 天天生鲜<pxd7th@vip.qq.com>


import djcelery

djcelery.setup_loader()
# rabbit-mq 配置
# BROKER_URL = 'amqp://guest@localhost//'
# CELERY_IMPORTS = ('celery_tasks.tasks_rabbitmq')
# # redis 配置
BROKER_URL = 'redis://127.0.0.1:6379/7'
CELERY_IMPORTS = ('celery_tasks.tasks_liuqi')  # 'amqp://guest@localhost//'

# 指定上传静态文件到fdfs 使用的存储类，FastDFSStorage自定义的存储类 django提供的无法满足
DEFAULT_FILE_STORAGE = 'utils.fastdfs.storage.FastDFSStorage'  # Storage最后

# 搭配自定义Storage使用的配置
CLIENT_CONF = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')

# 搭配Storage
SERVER_IP = 'http://192.168.247.128:8888/'

# 富文本样式配置
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',  # 丰富样式
    'width': 600,
    'height': 400,
}
