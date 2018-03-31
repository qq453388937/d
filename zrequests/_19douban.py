# -*- coding:utf-8 -*-
import requests
import json

"""
目标:
爬取豆瓣网电视信息
1 电视名称，封面信息 评分等
"""


class DouBanCrawl(object):

    def __init__(self):
        self.url = "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BE%8E%E5%89%A7&sort=recommend&page_limit=20&page_start=0"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

        }

        self.file = open("./douban.json", "w")

    def __del__(self):
        self.file.close()

    def get_data(self):
        response = requests.get(url=self.url, headers=self.headers)
        # print(response.content.decode())
        return response.content.decode()

    def parse_data(self, str):
        dict_data = json.loads(str)
        temp_arr = []
        for item in dict_data["subjects"]:
            model = dict()
            model["title"] = item["title"]
            model["rate"] = item["rate"]
            model["url"] = item["url"]
            temp_arr.append(model)
            # print(model)
        return temp_arr  # [{'rate': '7.5', 'url': 'https://movie.douban.com/subject/25814668/', 'title': '副本'},{},]

    def save_data(self, data_list):
        for item in data_list:
            self.file.write(json.dumps(item, ensure_ascii=False) + ",\n")

    def run(self):
        # 构建请求头
        # 发送请求 获取数据
        json_str = self.get_data()
        # 解析数据
        dict_list = self.parse_data(json_str)
        # 保存文件
        self.save_data(dict_list)


if __name__ == '__main__':
    douban = DouBanCrawl()
    douban.run()
