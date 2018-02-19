# -*- coding:utf-8 -*-
from itsdangerous import *

"""
JSON Web Tokens简称jwt，是rest接口的一种安全策略。本身有很多的优势：
    解决跨域问题：这种基于Token的访问策略可以克服cookies的跨域问题。
    服务端无状态可以横向扩展，Token可完成认证，无需存储Session。
    系统解耦，Token携带所有的用户信息，无需绑定一个特定的认证方案，只需要知道加密的方法和密钥就可以进行加密解密，有利于解耦。
    防止跨站点脚本攻击，没有cookie技术，无需考虑跨站请求的安全问题
"""
# 简单签名
s1 = Signer('secret-key')
ret = s1.sign('my string, ssssssssss,dddddddddddddlsd453388937'.encode())  # 签名需要encode为字节
print(type(ret))
print(ret)
print(ret.decode())
# print(type(ret.decode()))  # 解签名可以传byte也可以传字符串但是最后是byte字节类型如需要为字符串需要decode()

try:
    jiema = s1.unsign(b'my string, ssssssssss,dddddddddddddlsd453388937.flkCijIROsNInZZiO3qAuH5BCIM')
except BadSignature as e:
    print("伪造签名")
    jiema = None
print(jiema)

# 带时间戳的签名
print('=======================')
s2 = TimestampSigner('secret-key')
ret = s2.sign('fooooccadwad')  # 发送方加密
print(s2)
ret2 = s2.unsign(ret, max_age=5)  # 发送方加时间限制
print(ret2)
# time.sleep(4)
ret3 = s2.unsign(ret, max_age=5)
print(ret3)

# 序列化签名
print('============序列化签名===========')
s3 = Serializer('secret-key')
ret = s3.dumps([1, 2, 3, 4])
print(ret)
ret2 = s3.loads(ret)
print(ret2)

# 四、带时间戳的序列化：
print('=========带时间戳的序列化==============')
s4 = TimedSerializer('secret-key')
ret = s4.dumps([1, 2, 3, 4])
print(ret)
ret2 = s4.loads(ret, 4)
print(ret2)
# time.sleep(3)
ret2 = s4.loads(ret)
print(ret2)
# URL安全序列化 不带时间戳同一个字符串序列的是一样的
print('*' * 80)
s = URLSafeSerializer('secret-key')
ret = s.dumps([1, 2, 3, 4])
ret = s.dumps([1, 2, 3, 4])  # 一样
print(ret)
print(s.loads(ret))
#  JSON Web签名
print('*' * 80)
s = JSONWebSignatureSerializer('secret-key')
print(s.dumps({"name": "pxd", "age": 18}))
print(s.dumps({"name": "pxd", "age": 18}))  # 一样
# JSON WEB 签名 带时间戳
s = TimedJSONWebSignatureSerializer('secret-key', expires_in=5)
# ret = s.dumps({"name": "pxd", "age": 18})
ret = s.dumps({"user_id": "123"})
time.sleep(4)
ret2 = s.loads(ret)
print(s.loads(ret))
print(ret2['user_id'])

#
