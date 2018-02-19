# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "453388937@qq.com"  # 用户名
mail_pass = "xviwmcrwncyxbggh"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格

sender = '453388937@qq.com'
receivers = ['453388937@qq.com', ]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText('<h1>a test for python</h1>', 'html', 'utf-8') # 'plain'
message['From'] = Header("天天生鲜<453388937@qq.com>", 'utf-8')
message['To'] = Header(receivers[0], 'utf-8')

subject = '天天生鲜用户激活666'  # 标题
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.quit()
    print("发送邮件成功")

except Exception as e:
    print(e)
