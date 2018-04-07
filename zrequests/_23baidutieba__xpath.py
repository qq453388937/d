# -*- coding:utf-8 -*-
import requests
from lxml import etree
import time
import os


class BaiduTieBa(object):
    """
    data = {'first': 'Hodor', 'last': 'Hodor!'}
    "{first}{last}".format(**data)
    """

    def __init__(self, name):
        self.url = "http://tieba.baidu.com/f?ie=utf-8&kw={}".format(name)
        self.headers = {
            # "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

            # 使用较老版本的请求头,该浏览器不支持javascript
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.01; WINDOW NT 5.0)",  # 上个世纪的浏览器js给注释了
            # 代码加注释,浏览器渲染把注释去了,获取源码的话是注释过的
        }

    def get_data(self, url):
        response = requests.get(url=url, headers=self.headers)
        return response.content.decode()

    def parse_data(self, data):
        # 创建etree对象,将文本转换称elements对象
        html = etree.HTML(data)
        # with open("test.html","w",encoding="utf-8") as f:
        #     f.write(data)
        # 使用xpath匹配
        ahref_node_list = html.xpath('//*[@id="thread_list"]/li[@class=" j_thread_list clearfix"]/div/div/div/div/a')
        print(ahref_node_list)
        # 遍历提取链接
        temp_list = []
        for item in ahref_node_list:
            temp = dict()
            temp["href"] = "http://tieba.baidu.com" + item.xpath("./@href")[0] if len(
                item.xpath("./@href")) else ""  # xpath肯定返回的是一个列表,没有数据会异常
            temp["title"] = item.xpath("./text()")[0] if len(item.xpath("./text()")) else ""  # xpath肯定返回的是一个列表,没有数据会异常
            # print(temp)
            temp_list.append(temp)

        # 提取下一页的节点
        next_page = html.xpath('//*[@id="frs_list_pager"]/a[last()-1]/@href')[0]
        print("http:" + next_page)
        next_page = "http:" + next_page
        return temp_list, next_page

    def parse_detial_page(self, data):
        # 解析详情页的html数据
        html = etree.HTML(data)  # 创建etree对象,将文本转换称elements对象
        # 提取图片
        # contains 的使用!!!!!!!!!!
        # teacher  html.xpath('//cc/div[contains(@class,"d_post")]/img[@class="BDE_Image"]')
        url_list = html.xpath('//*[@class="d_post_content j_d_post_content  clearfix"]/img/@src')
        print(url_list)
        return url_list

    def save_images(self, url_list):
        for url in url_list:
            image_data = requests.get(url, headers=self.headers).content
            name = str(time.time()) + ".jpg"
            # os.sep  /  | \\
            if not os.path.exists("images"):
                os.makedirs("images")
            with open("./images/" + name, "wb") as f:
                f.write(image_data)
                print("存了一个图片!")
        print("一个帖子图片存储完毕!!")

    def run(self):
        # 构造url和请求头 ,第一页
        # dowhile 循环做法
        content = self.get_data(self.url)
        while True:
            # 发送请求获取html\
            data_list, next_page = self.parse_data(content)  # 返回详情页的url和标题,和下一页的链接
            # 解析数据,返回列表数据,详情页的数据,获取详情页图片的链接
            for x in data_list:
                url = x["href"]
                detail_html = self.get_data(url)  # 获取详情页的html
                url_list = self.parse_detial_page(detail_html)  # 返回详情页所有的图片链接列表
                # 存储数据 下载图片 根据传入的列表
                self.save_images(url_list)
            content = self.get_data(next_page)  # 获取下一页,返回下一页详情的url和标题

        # next_page = self.url
        # while True:
        #     content = self.get_data(next_page)
        #     # 发送请求获取html\
        #     data_list, next_page = self.parse_data(content)  # 返回详情页的url和标题,和下一页的链接
        #     # 解析数据,返回列表数据,详情页的数据,获取详情页图片的链接
        #     for x in data_list:
        #         url = x["href"]
        #         detail_html = self.get_data(url)  # 获取详情页的html
        #         url_list = self.parse_detial_page(detail_html)  # 返回详情页所有的图片链接列表
        #         # 存储数据 下载图片 根据传入的列表
        #         self.save_images(url_list)
        #     content = self.get_data(next_page)  # 获取下一页,返回下一页详情的url和标题



if __name__ == '__main__':
    baidu = BaiduTieBa("旅行吧")
    baidu.run()
