# -*- coding:utf-8 -*-
import requests

url = 'http://www.baidu.com/'
proxies = {
    'http': 'http://175.20.211.18:8060',
    'https': 'https://175.20.211.18:8060'
}

# # 付费代理,用户名：密码@ip和port
# 付费代理,用户名:密码@ip和port
# proxies = {
#     'http':'http://user:pwd@115.223.200.85:9000' # http基于
# }

response = requests.get(url, proxies=proxies)
print(response.text)
