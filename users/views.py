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
from itsdangerous import TimedJSONWebSignatureSerializer
# 导入celery中的异步方法
# from celery_tasks.tasks import send_active_email  # send_active_email方法和远程服务器方法两份
# 导入刘琦的异步方法
from celery_tasks.tasks_liuqi import send_active_email


# 导入rabbitmq 的celery
# from celery_tasks.tasks_rabbitmq import send_active_email


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


# def send_active_email(to_email, user_name, token):
#     """封装发送邮件方法"""
#     subject = "天天生鲜用户激活666"  # 标题
#     body = ""  # 纯文本邮件体写这里
#     from django.conf import settings  # 导入settings,方便粘贴方法不用考虑引用问题
#     sender = settings.EMAIL_FROM  # 发件人
#     receiver = [to_email]  # 接收人,可以多个
#     html_body = '<h1>尊敬的用户 %s, 感谢您注册天天生鲜！</h1>' \
#                 '<br/><p>请点击此链接激活您的帐号<a href="http://127.0.0.1:8000/users/active/%s">' \
#                 'http://127.0.0.1:8000/users/active/%s</a></p>' % (user_name, token, token)
#     from django.core.mail import send_mail  # 发送邮件方法 方便粘贴方法不用考虑引用问题
#     send_mail(subject, body, sender, receiver, html_message=html_body)  # html字符串写这里


# 类视图
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

        # s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=3600)
        # token = s.dumps({"user_id": user.id}).decode() 下面做了封装
        # 使用itsdangerous签名token
        token = user.generate_active_token()  # 封装方法返回字符串
        print("发送邮件开始")
        # send_active_email(email, user_name, token) # 同步的时候调用

        # 正确写法 异步调用
        send_active_email.delay(email, user_name, token)
        print("发送邮件成功")
        return HttpResponse("注册成功! 稍后查看邮件激活!")

        # return redirect(reverse('users:login'))


class ActiveView(View):
    """邮件激活"""

    def get(self, request, token):
        """处理激活请求"""
        from itsdangerous import TimedJSONWebSignatureSerializer
        from django.conf import settings
        from itsdangerous import SignatureExpired, BadSignature
        # 取的时候和expire参数无关,expire只对设置的dumps有效,是一个全新的序列化器

        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY)

        try:
            dict = serializer.loads(token)
        except (SignatureExpired, BadSignature) as e:  # 捕获多个异常,超时和签名失败
            return HttpResponse("激活失败")
        user_id = dict.get("user_id", "没取到")
        print(user_id)
        user_model = User.objects.get(id=user_id)
        user_model.is_active = True
        user_model.save()

        return redirect(reverse('users:login'))


class Login(View):
    def get(self, request):
        """登陆页面展示"""
        return render(request, "login.html")

    def post(self, request):
        """处理登陆逻辑"""
        from django.contrib.auth import authenticate, login
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if not all([username, password]):
            # return render(request, 'login.html', {'err_msg': '用户名密码不能为空'})
            return redirect(reverse('users:login'))
        user = authenticate(username=username, password=password)  # django自带校验
        is_ok = False
        if user is not None:
            if user.is_active:
                login(request, user)
                is_ok = True
            else:
                return render(request, 'login.html', {'err_msg': '用户未激活,请查看邮件激活!'})
        else:
            return render(request, 'login.html', {'err_msg': '用户名或密码错误!'})
        if is_ok:
            
            """
        一键多值,session id 单个,和cookie中sessionid的值一致
        fd2dac6bce19f55aeb4e267f0ccad4b22a94d338:{"_auth_user_id":"49","_auth_user_backend":"django.contrib.auth.backends.ModelBackend","pxd_name":"\u88f4\u6653\u4e1c666666","_auth_user_hash":"a28292554ea826aa5113a9cf4bd9810b5b4499b8"}
            """
            request.session['pxd_name'] = '裴晓东666666'
            return HttpResponse("ok")
