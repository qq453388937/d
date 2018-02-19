"""
Django settings for d project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

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
    # 安装应用
    #  django 用户认证系统规定,安装的应用名称需要和 'AUTH_USER_MODEL = 'users.User'' 单应用
    'users',
    'goods',
    'orders',
    'cart',

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# 配置静态文件加载路径
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    # 这句话的意思是默认去找static文件夹下的[和项目同名的=>booktest文件夹非必须]
    os.path.join(BASE_DIR, 'static')
]

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

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 导入邮件模块
# EMAIL_HOST = 'smtp.163.com'  # 发邮件主机 smtp.yeah.net
# EMAIL_PORT = 25  # 发邮件端口 wofedmnlmegjcaca 25
# EMAIL_HOST_USER = '15346566750@163.com'  # 授权的邮箱 pxd7th@vip.qq.com
# EMAIL_HOST_PASSWORD = 'wy2921481'  # 邮箱授权时获得的密码，非注册登录密码
# EMAIL_FROM = '天天生鲜<15346566750@163.com>'  # 发件人抬头 天天生鲜<pxd7th@vip.qq.com>

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 导入邮件模块
EMAIL_HOST = 'smtp.qq.com'  # 发邮件主机 smtp.yeah.net
EMAIL_PORT = 465  # 发邮件端口 wofedmnlmegjcaca 25
EMAIL_HOST_USER = '453388937@qq.com'  # 授权的邮箱 pxd7th@vip.qq.com
EMAIL_HOST_PASSWORD = 'pxd0015193111827'  # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = '天天生鲜<453388937@qq.com>'  # 发件人抬头 天天生鲜<pxd7th@vip.qq.com>
