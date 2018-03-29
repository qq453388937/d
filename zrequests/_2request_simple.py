# -*- coding:utf-8 -*-
# 发送get请求百度首页

# 导入requests
import requests

# 构造url
url = 'http://www.baidu.com/'

# 发送请求
response = requests.get(url)

# 输出响应的数据str
print(response.text)
# 输出响应的编码格式
print(response.encoding)
print('---------------')
# 输出响应的数据bytes
print(response.content)

# 手动修改响应的编码格式
response.encoding = 'utf8'
print (response.text)

# 直接把响应数据改成utf8
print(response.content.decode())

# 获取响应的状态码
print(response.status_code)

# 获取响应的url
print(response.url)


# 获取响应中的请求信息
print(response.request.headers)

# 获取响应头
print(response.headers)
