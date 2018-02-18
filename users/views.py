from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# 类视图需要
from django.views.generic import View
# 反向解析
from django.core.urlresolvers import reverse
import re
# 模型类
from users.models import User
# 异常===> 重名
from django.db import IntegrityError
# 配置文件的导入
from django.conf import settings
# itsdangerous导入  并且起别名
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeSerializer as Serializer

# Create your views here.


def register(request):
    """
    注册逻辑
    127.0.0.1:8000/users/register/ ../static/css/reset.css
    127.0.0.1:8000/users/static/css/reset.css
    127.0.0.1:8000/users/register ../static/css/reset.css #最后一个/ zuo是当前文件夹
    127.0.0.1:8000/static/css/reset.css

    """

    if request.method == "GET":
        return render(request, "register.html")  # 天天生鲜里不再使用应用去区分模板
    elif request.method == "POST":
        return HttpResponse("测试")


# 类视图
def send_active_email(to_email, user_name, token):
    """封装发送邮件方法"""
    subject = "天天生鲜用户激活666"  # 标题
    body = ""  # 文本邮件体
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [to_email]  # 接收人,可以多个
    html_body = '<h1>尊敬的用户 %s, 感谢您注册天天生鲜！</h1>' \
                '<br/><p>请点击此链接激活您的帐号<a href="http://127.0.0.1:8000/users/active/%s">' \
                'http://127.0.0.1:8000/users/active/%s</a></p>' % (user_name, token, token)
    from django.core.mail import send_mail
    send_mail(subject, body, sender, receiver, html_message=html_body)


class RegisterView(View):
    """from django.views.generic import View"""
    """from django.views.generic import View"""

    def get(self, request):  # request紧跟其后就可以了
        return render(request, "register.html")

    def post(self, request):
        # 1.接受用户输入
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        print(user_name)
        print(allow)  # checkbox: on | None
        # 2.校验用户输入  拦截性操作取反
        # all 一假为假
        if not all([user_name, pwd, email]):  # , allow 如果在里面会直接跳转无提示
            # not True 校验不通过
            return redirect(reverse('users:register'))  # 刷新
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'err_msg': '服务端校验：邮箱格式错误'})
        if not allow:
            return render(request, 'register.html', {'err_msg': '服务端校验：请同意用户协议!'})
        # 传统的添加
        # User.objects.create(
        #     email='123@qq.com',
        #     user_name='pxd',
        #
        # )
        # user = User()
        # user.email='123@qq.com'
        # user.save()
        # 3.校验成功创建用户，保存用户数据
        # 由于User 继承自AbstractUser 所以不用导入from django.contrib.auth.models import Yser
        try:
            user = User.objects.create_user(user_name, email, pwd)
        except IntegrityError as e:
            return render(request, 'register.html', {'err_msg': '用户已存在'})
        user.is_active = False  # django 默认激活我们这里用邮件激活的方式所以不激活
        user.save()  # 重新保存

        # 保存成功后发送邮件激活！
        # 发送邮件http://127.0.0.1/users/active/user_id  user_id 利用签名混淆
        from django.core.mail import send_mail
        # token


        send_active_email(email, user_name, '')
        return HttpResponse("测试成功")


class ActiveView(View):
    """邮件激活"""

    def get(self, request, token):
        """处理激活请求"""
        pass
