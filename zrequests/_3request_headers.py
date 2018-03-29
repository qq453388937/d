# -*- coding:utf-8 -*-
# 发送带请求头的参数
import requests

url = 'http://www.baidu.com/'

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}

# 发送带请求头的请求
response1 = requests.get(url, headers=headers)
response2 = requests.get(url)
print(len(response1.text))
print(len(response2.text))

with open('baidu1.html', 'wb') as f:
    f.write(response1.content)

with open('baidu2.html', 'wb') as f:
    f.write(response2.content)
