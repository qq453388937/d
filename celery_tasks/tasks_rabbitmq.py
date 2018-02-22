# -*- coding:utf-8 -*-
from celery import task


@task
def send_active_email(to_email, user_name, token):
    """封装发送邮件方法"""
    import time
    time.sleep(10)
    subject = "天天生鲜用户激活666_刘琦版本"  # 标题
    body = ""  # 纯文本邮件体写这里
    from django.conf import settings  # 导入settings,方便粘贴方法不用考虑引用问题
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [to_email]  # 接收人,可以多个
    html_body = '<h1>尊敬的用户 %s, 感谢您注册天天生鲜！</h1>' \
                '<br/><p>请点击此链接激活您的帐号<a href="http://127.0.0.1:8000/users/active/%s">' \
                'http://127.0.0.1:8000/users/active/%s</a></p>' % (user_name, token, token)
    from django.core.mail import send_mail  # 发送邮件方法 方便粘贴方法不用考虑引用问题
    send_mail(subject, body, sender, receiver, html_message=html_body)  # html字符串写这里
