# -*- coding:utf-8 -*-
import requests

# url = 'https://www.12306.cn/mormhweb/'

# url = 'http://www.youtube.com/'

url = 'http://www.baidu.com'
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}

# verify设置ssl不认证，设置后会有警告信息
# response = requests.get(url, verify=False)

# 设置请求的超时时间，单位是s
# response = requests.get(url,timeout=3)

response = requests.get(url, headers=headers)
# 获取cookie信息
# print(response.cookies)

# 把cookie转成字典
content = requests.utils.dict_from_cookiejar(response.cookies)
print(content)
# 将cookie字典转成对象
c = requests.utils.cookiejar_from_dict(content)
print(c)


