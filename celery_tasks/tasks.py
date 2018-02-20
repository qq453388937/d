# -*- coding:utf-8 -*-
# django初始化不然找不到settings,django项目中不能写
# import os
# os.environ["DJANGO_SETTINGS_MODULE"] = "d.settings"
# # 放到Celery服务器上时添加的代码
# import django
# django.setup()

# 创建celery对象/客户端
from celery import Celery


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
