# -*- coding:utf-8 -*-
import requests
import json, re


class Kr36(object):

    def __init__(self):
        self.url = "http://36kr.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        self.file = open("kr.json", "w", encoding="utf-8")

    def get_data(self):
        response = requests.get(url=self.url, headers=self.headers)
        return response.content.decode()

    def parse_data(self, data):
        """data假设为数据字符串"""
        # dict_data = json.loads(data)
        # with open("36kr.html", "w",encoding="utf-8") as f:
        #     f.write(data)
        partial_str = re.findall("<script>var props=(.*})</script>", data, re.S)[0]
        result_str = re.sub(",locationnal={.*", '', partial_str)  # data中所有匹配,locationnal={.*的替换为""空字符串
        my_dict = json.loads(result_str)
        # print(my_dict)
        temp_arr = []
        print("*" * 20)
        # 新闻在"feedPostsLates|post" 的键里
        for item in my_dict["feedPostsLatest|post"]:
            temp = {}
            temp["url"] = item["cover"]
            temp["title"] = item["title"]
            print(temp)
            temp_arr.append(temp)
        return temp_arr
        # print(result)

    def save_data(self, data_list):
        for item in data_list:
            self.file.write(json.dumps(item, ensure_ascii=False)+",\n")

    def __del__(self):
        self.file.close()

    def run(self):
        # 构造请求的url和请求头
        # 发送请求获取网页数据
        html = self.get_data()
        # print(html)
        # 解析数据
        arr = self.parse_data(html)
        # 存储(.json)
        self.save_data(arr)

        pass


if __name__ == '__main__':
    kr36 = Kr36()
    kr36.run()
