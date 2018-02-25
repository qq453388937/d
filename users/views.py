from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# 类视图需要
from django.views.generic import View, TemplateView
# 反向解析
from django.core.urlresolvers import reverse
import re
# 模型类
from users.models import *  # User,Address
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


# 导入登陆校验模块的装饰器
from django.contrib.auth.decorators import login_required
# 导入工具类模块的登陆校验类
from utils.views import MyLoginBaseViewMixin  # 导入工具类模块的登陆校验类


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

    def post(self, request):  # request紧跟其后就可以了
        # 1.接受用户输入 #  request.GET 是获取?后面的东西区分请求方式!!!!!!!!!!!!!!!
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        print(user_name)
        print(allow)  # checkbox: on | None
        # 2.校验用户输入  拦截性操作取反
        # all 一假为假 ,any 一真为真
        if not all([user_name, pwd, email]):  # , allow 如果在里面会直接跳转无提示
            # not True 校验不通过
            return redirect(reverse('users:register'))  # 刷新
        #  邮箱正则
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

        # 正确写法 异步调用 异步发送激活邮件
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

        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=3600)

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
        user_name = request.COOKIES.get('user_name', None)
        return render(request, "login.html", {'user_name': user_name})

    def post(self, request):
        """处理登陆逻辑
        set_cookie(key, value='', max_age=None, expires=None)：设置Cookie
            key、value都是字符串类型
            max_age是一个整数，表示在指定秒数后过期
            expires是一个datetime或timedelta对象，会话将在这个指定的日期/时间过期，注意datetime和timedelta值只有在使用PickleSerializer时才可序列化
            max_age与expires二选一
            如果不指定过期时间，则两个星期后过期
        """
        from django.contrib.auth import authenticate, login
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if not all([username, password]):  # 一假为假 not 拦截判断
            # return render(request, 'login.html', {'err_msg': '用户名密码不能为空'})
            return redirect(reverse('users:login'))
        user = authenticate(username=username, password=password)  # django自带校验用户名和密码，通过不为None
        is_ok = False
        if user is not None:
            if user.is_active:
                login(request, user)  # 会存储session 状态保持,会根据存储引擎的不同存储位置也不同
                is_ok = True
                # 记住用户名,免登录10 天, 反正保存到浏览器关闭 开始－－－－－－－－－－－
                ret_remember = request.POST.get('remembered')
                print(ret_remember)  # 打印是否为on
                http_response = HttpResponse()
                http_response.content = "ok！登陆成功手动设置HttpResponse"
                # 保存到浏览器关闭,浏览会话结束时  checkbox: on | None ---------------------------------
                if ret_remember != "on":
                    request.session.set_expiry(0)
                else:  # 保存10天 点击了记住 if分支
                    http_response.set_cookie("user_name", username, max_age=60 * 60 * 24 * 1)
                    request.session.set_expiry(60 * 60 * 24 * 10)
                # ------------------------------------------------------------------------------------------
                # 在这里也可以登陆成功以后判断页面的跳转，移动到if is_ok 的分支
            else:
                return render(request, 'login.html', {'err_msg': '用户未激活,请查看邮件激活!'})
        else:
            return render(request, 'login.html', {'err_msg': '用户名或密码错误!'})
        if is_ok:
            """一键多值,session id 单个,和cookie中sessionid的值一致
            fd2dac6bce19f55aeb4e267f0ccad4b22a94d338:{"_auth_user_id":"49","_auth_user_backend":"django.contrib.auth.backends.ModelBackend","pxd_name":"\u88f4\u6653\u4e1c666666","_auth_user_hash":"a28292554ea826aa5113a9cf4bd9810b5b4499b8"}
            """
            # 测试存储一个session的值而已,可以存储一下已登陆的用户名信息方便展示使用
            request.session['pxd_name'] = 'MMD666666'
            next = request.GET.get('next')
            if next:  # next有值
                return redirect(next)
            else:  # 跳转到主页，主页待补全功能后跳转
                return http_response


class Logout(View):
    def get(self, request):
        """
        需要清理服务器的session数据
        需要清理浏览器的cookie数据
        """
        from django.contrib.auth import authenticate, login, logout
        logout(request)
        return redirect(reverse('users:login'))  # 退出登陆后进入登录页面


# @login_required  # 类上面加方法错误!!!
from utils.views import MyLoginBaseViewMixin  # 导入工具类模块的登陆校验类


class AddressView(MyLoginBaseViewMixin, View):
    # @login_required  # 方法上加装饰器错误!!!
    # @classmethod  错误!!!
    # def as_view(cls, **initkwargs):
    #     super(Address, )
    def get(self, request):
        print(Address.__mro__)  # c3 算法搜索方法顺序
        """提供收货地址页面，查询地址信息，提供修改功能渲染
        # 原始写法判断用户是否登陆 request.user.is_authenticated() 登陆返回True
        if not request.user.is_authenticated():
            return redirect(reverse('users:login'))
        else
            return render(request,'user_center_site.html')
        """
        # 获取登陆用户
        login_user = request.user  # 登陆后request.user不为None，因为该视图继承MyLoginBaseViewMixin，经过登陆校验的
        # add = Address.objects.filter(user=login_user).order_by('-create_time')[0]
        # address_lastest_model0 = Address.objects.filter(user=login_user)[-1]
        # address_lastest_model = Address.objects.filter(user=login_user).order_by('-create_time')[0]
        # address_lastest_model2 = login_user.address_set.order_by('-create_time')[0]
        try:
            # 查询用户的地址信息，取最新最近创建的地址信息

            address_lastest_model3 = login_user.address_set.latest('create_time')  # 默认倒叙
        except Exception as e:
            address_lastest_model3 = None  # None模板判断使用
        print(address_lastest_model3)
        # 构造上下文
        context = {
            # 'user': login_user, # django已经封装给一个对象 user 在 request 中不用传递，并且前台直接可以user点出来
            'address': address_lastest_model3,
        }
        # 渲染模板
        # if request.user.is_authenticated()

        return render(request, 'user_center_site.html',context)



    def post(self, request):
        recv_name = request.POST.get('recv_name')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        recv_mobile = request.POST.get('recv_mobile')
        if all([recv_name, addr, zip_code, recv_mobile]):
            # 正则等校验略过 re模块
            Address.objects.create(
                # user=request.user,
                user_id=request.user.id,
                receiver_name=recv_name,
                detail_addr=addr,  # name和字段不一致
                zip_code=zip_code,
                receiver_mobile=recv_mobile,
            )
        return redirect(reverse('users:address'))


class UserInfoView(MyLoginBaseViewMixin, View):
    def get(self, request):
        """查询个人信息和最近浏览信息"""
        # 能进来get肯定是登陆的用户因为继承了MyLoginBaseViewMixin 已经做过了登陆session 校验
        login_user = request.user
        try:
            user_lastest_address = Address.objects.filter(user=login_user).order_by('-create_time')[0]
        except Address.DoesNotExist:
            user_lastest_address = None

        context = {
            'user_lastest_address_model': user_lastest_address_model # dawdawdawdwadawdawdawdawd
        }
        return render(request, 'user_center_info.html', context) # wwoewdwadwadwadwadwa

