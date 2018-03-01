# -*- coding:utf-8 -*-
# django初始化不然找不到settings,django项目中不能写
# import os
# os.environ["DJANGO_SETTINGS_MODULE"] = "d.settings"
# # 放到Celery服务器上时添加的代码
# import django
# django.setup()

import os

# 创建celery对象/客户端
from celery import Celery

from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.template import loader, RequestContext  # 常规写法导包使用
from django.http import HttpResponse
from goods.models import *
from django.conf import settings

# 1.参数1指定任务所在的路径从包名开始
# 2.参数2指定任务队列broker,可以作为任务队列的有多种,此处以redis数据库为例
app = Celery("celery_tasks.tasks", broker="redis://127.0.0.1:6379/4")


# 3.生产任务 就是
@app.task  # ===> app.task(send_active_email)  装饰就是method
def send_active_email(to_email, user_name, token):
    """封装发送邮件方法"""
    import time
    time.sleep(10)
    subject = "天天生鲜用户激活666"  # 标题
    body = ""  # 纯文本邮件体写这里
    from django.conf import settings  # 导入settings,方便粘贴方法不用考虑引用问题
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [to_email]  # 接收人,可以多个
    html_body = '<h1>尊敬的用户 %s, 感谢您注册天天生鲜！</h1>' \
                '<br/><p>请点击此链接激活您的帐号<a href="http://127.0.0.1:8000/users/active/%s">' \
                'http://127.0.0.1:8000/users/active/%s</a></p>' % (user_name, token, token)
    from django.core.mail import send_mail  # 发送邮件方法 方便粘贴方法不用考虑引用问题
    send_mail(subject, body, sender, receiver, html_message=html_body)  # html字符串写这里


@app.task
def generic_static_index_html():
    """
    异步生成静态主页，运维改了之后调用该异步方法生成静态主页
    用户访问index.html：80 是未登陆状态下是不需要购物车和登陆信息的
    只需要渲染html，只需要上下文和模板， 不需要user，request等信息
    """
    # 查询用户ｕｓｅｒ信息 ,不需要 在request中

    # 查询商品分类信息
    categorys = GoodsCategory.objects.all()
    # 查询图片轮播信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')
    # 查询商品活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
    # 查询主页分类商品列表信息
    for category in categorys:
        # 分组查询出来 ,六大分类
        title_banners = IndexCategoryGoodsBanner.objects.filter(category=category).filter(display_type=0)
        category.title_banners = title_banners  # 动态的添加对象的属性 ,for 循环一次每个对象动态的添加一个属性
        image_banners = IndexCategoryGoodsBanner.objects.filter(category=category).filter(display_type=1)
        category.image_banners = image_banners  # 动态的添加对象的属性 ,for 循环一次每个对象动态的添加一个属性
    # 查询购物车信息
    cart_num = 88
    # 构造上下文
    context = {
        'categorys': categorys,
        'goods_banners': goods_banners,
        'promotion_banners': promotion_banners,
        'cart_num': cart_num,
    }
    # 获取模板
    template = loader.get_template('static_index.html')  # 动态有动态的base 静态有静态的base ,静态base干掉用户校验导航栏部分,静态index修改extends
    # 渲染模板
    html_data_str = template.render(context)
    # 模板保存到celery服务器  static/ 用一下django的settings的static静态路径
    path = os.path.join(settings.STATICFILES_DIRS[0], 'index.html')
    with open(path, 'w') as f:
        f.write(html_data_str)


def test(request):
    """常规写法"""
    # 定义上下文
    context = RequestContext(request, {'key': 'value'})
    context = {'key': 'value'}
    # 获取模板
    template = loader.get_template('Booktest/index.html')
    # 渲染模板 template.render(context) 就是即将要渲染的html字符串
    return HttpResponse(template.render(context))
