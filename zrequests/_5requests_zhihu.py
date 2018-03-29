# -*- coding:utf-8 -*-
import requests,time

url = "https://www.zhihu.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}

data = {
    "wd": "python"
}

response = requests.get(url, headers=headers, params=data)

print(response.status_code)
print(response.text)

#
# with open("%s" % "baidu.com", "wb") as f:
#
#    f.write(response.content)
