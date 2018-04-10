# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup

# pip install bs4
# pip install beautifulsoup4

url = "http://hr.tencent.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}
response = requests.get(url, headers=headers)
html = response.content.decode()
# print(response.content.decode())
# 创建beautiful Soup 对象
soup = BeautifulSoup(html, "lxml") # 指定解析器后python2就不会报错了
# soup = BeautifulSoup(open("index.html"))_
# print(soup.prettify()) # 美化输出
print(soup.title)
