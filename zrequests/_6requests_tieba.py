# -*- coding:utf-8 -*-
import requests, time


# format
class Baidu(object):
    def __init__(self, name, pn):
        """f?kw = 李毅 & ie = utf - 8 & tp = 0 & pn = 50"""
        self.name = name
        self.url = "https://tieba.baidu.com/f/good?kw={}&ie=utf-8&pn=".format(self.name)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        self.data = {}
        self.url_list = [self.url + str(pn * 50) for pn in range(pn)]

        print(self.url_list)

    def get_data(self, url):
        response = requests.get(url=url, headers=self.headers)
        # print(response.content.decode())
        return response.content  # 返回二进制

    def save_data(self, data, num):
        # with open("tieba.html", "wb") as f:
        #     f.write(data)
        file_name = self.name + "_" + str(num) + ".html"
        with open(file_name, "wb") as f:
            f.write(data)

    def run(self):
        for url in self.url_list:
            data = self.get_data(url)
            index = self.url_list.index(url)
            self.save_data(data, index)


class Baidu(object):
    def __init__(self, name, pn):
        self.name = name
        self.url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn=".format(name)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }
        self.url_list = [self.url + str(pn * 50) for pn in range(pn)]
        print(self.url_list)

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def save_data(self, data, num):
        file_name = self.name + "_" + str(num) + ".html"
        with open(file_name, "wb") as f:
            f.write(data)

    def run(self):
        for url in self.url_list:
            data = self.get_data(url)
            index = self.url_list.index(url)  # 列表有个index(元素) 返回索引
            self.save_data(data, index)


import sys

if __name__ == '__main__':
    name = sys.argv[1]
    pn = int(sys.argv[2])
    baidu = Baidu(name, pn)
    baidu.run()
#
# with open("%s" % "baidu.com", "wb") as f:
#
#    f.write(response.content)
