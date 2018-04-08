# -*- coding:utf-8 -*-
import requests
from lxml import etree
import json


class QiuShiBaike(object):
    """
    抓取用户名,性别,年龄,用户个人信息页
    """

    def __init__(self):
        self.url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.url_list = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

            # 使用较老版本的请求头,该浏览器不支持javascript
            # "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.01; WINDOW NT 5.0)",  # 上个世纪的浏览器js给注释了
        }
        self.file = open("qiushibaike.json", "w")

    # 定义方法用来生成url 列表
    def genrate_url_list(self):
        self.url_list = [self.url.format(i) for i in range(1, 14)]

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content  # 测试是否decode()

    def parse_data(self, data):
        # 创建etree 对象 将文本转换称elements对象
        html = etree.HTML(data)
        # 使用xpath提取节点列表
        node_list = html.xpath('//*[contains(@class,"article block untagged mb15")]')
        # print(node_list)
        temp_arr = []
        for node in node_list:
            # 可以try except 更加简单
            temp_dict = {}
            temp_dict["content"] = node.xpath('./a[1]/div/span[1]/text()')[0]
            temp_dict["user_name"] = node.xpath('./div/a/h2/text()|./div/span/h2/text()')[0]
            # 性别包含在class属性中
            if_str = str(node.xpath("//div[contains(@class,'articleGender')]/@class")[0])
            if "woman" in if_str:
                temp_dict["gender"] = "woman"
            else:
                temp_dict["gender"] = "man"
            temp = node.xpath("./div/a/@href")
            if temp:
                temp_dict["user_url"] = temp[0]
            else:
                temp_dict["user_url"] = ""
            temp_arr.append(temp_dict)
        return temp_arr

    def save_data(self, dict_data):
        self.file.write(json.dumps(dict_data, ensure_ascii=False) + "\n,")

    def __del__(self):
        self.file.close()

    def run(self):
        # 1. 构造请求url和请求头
        # 2. 生成url列表
        self.genrate_url_list()
        print(self.url_list)
        # 3. 发送请求获取响应 循环执行发送请求,传入生成的url列表中的具体页数
        for url in self.url_list:
            data = self.get_data(url)
            # 4.解析参数
            data_dict = self.parse_data(data)
            # 5. 保存数据 ,如果响应数据是json字符串,想要获取指定数据的时候,一般需要转换成字典,提取数据,如果需要写文件,需要dumps
            self.save_data(data_dict)

if __name__ == '__main__':
    qs = QiuShiBaike()
    qs.run()
