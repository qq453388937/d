# -*- coding:utf-8 -*-
import requests
import re
import json
import time


class NeiHan(object):

    def __init__(self):
        self.url = "http://neihanshequ.com/"
        self.ajax_url = "http://neihanshequ.com/joke/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

        }

        self.file = open("neihan.json", "w", encoding="utf8")
        # <a target="_blank" class="image share_url" href="(.*?)" data-group-id=".*?">  .*?<p>(.*?)</p>

    def __del__(self):
        self.file.close()  # 关闭文件

    def get_data(self, url=None, params=None):
        if params is None:
            response = requests.get(url, headers=self.headers)
        else:
            self.headers[
                "Cookie"] = 'csrftoken=315eecbd45578d949847422a64941c62; tt_webid=6539079938367211011; uuid="w:079909cff7304b36bec6ecfdb4431a09"; _ga=GA1.2.1355956407.1522498194; _gid=GA1.2.1904668912.1522498194; _gat=1'
            response = requests.get(url, headers=self.headers, params=params)

        # print(response.content.decode())  # 打印首页内容
        return response.content.decode()

    def save_data(self, data, params=None):
        if params is None:
            for item in data:
                self.file.write(json.dumps(item, ensure_ascii=False) + ",\n")
        else:
            for item in data:
                self.file.write(json.dumps(item, ensure_ascii=False) + ",第二页后面的\n")

    """
        <a target="_blank" class="image share_url" href=".*" data-group-id=".*?">.*?<p>.*?</p>
    """

    def parse_data(self, html):
        """格式化数据,返回处理后的数据和时间戳"""
        # 根据正则分组来提取段子数据,findall只会提取括号中的数据
        re_array = re.findall(
            r'<a\s*target="_blank"\s*class="image share_url"\s*href="(.*?)"\s*data-group-id=".*?" >.*?<p>(.*?)</p>',
            html, re.S)  # 如果分组会放到一个元祖里[(group1,group2,group3)]
        # print(len(re_array))
        # print(re_array)
        # print(type(re_array))
        # print(re_array[0])
        """[(group1,group2,group3),(group1,group2,group3),....]  ==>  [{"url":"","content":""},]"""
        temp_arr = []
        for x in re_array:
            model = dict()
            model["url"] = x[0]  # 第一组
            model["content"] = x[1]  # 第二组
            # print(model)  # 打印字典
            temp_arr.append(model)
        # print(temp_arr) # 打印列表
        timestamp = re.search(r"max_time:\s*'(.*?)',", html, re.S).group(1)
        # re.findall 如果只有一个括号,是列表里面字符串,如果超过一个括号是列表里面嵌套元祖!!!!!!
        timestamp_tech = re.findall(r"max_time:\s*'(.*?)',", html, re.DOTALL)[0]  # 一个括号['','',''] 多个[('',''),('','')]
        # print(timestamp)
        # print(timestamp_tech)
        return temp_arr, timestamp

    def parse_ajax_data(self, json_str):
        my_dict = json.loads(json_str)
        # print(my_dict["data"])
        temparr = []
        for item in my_dict["data"]["data"]:
            model = dict()
            model["text"] = item["group"]["text"]
            model["share_url"] = item["group"]["share_url"]
            print(model)
            temparr.append(model)
        # print("*\n" * 30)
        # print(temparr)
        timstamp = my_dict["data"]["max_time"]

        return temparr, timstamp

    def run(self):
        """首页会生成时间戳,作为加载下一页的GET参数"""
        # 构造 url 请求头 __init__
        # 发送请求,获取响应html
        html = self.get_data(self.url)
        # 解析数据
        data, timestamp = self.parse_data(html)
        # 保存文件
        self.save_data(data)
        paramas = {
            "is_json": 1,
            "app_name": "neihanshequ_web",
        }
        # 发送ajax请求获取下一页数据!
        page = 1
        while True:
            time.sleep(0.5)
            page += 1
            paramas["max_time"] = timestamp
            html_next_page = self.get_data(self.ajax_url,
                                           paramas)  # [{'share_url':'text': ''},{'share_url':'text': ''}]
            ajax_data, timestamp = self.parse_ajax_data(html_next_page)
            self.save_data(ajax_data, "json")
            print("段子第%s页" % page)
            if len(ajax_data) == 0:
                break


if __name__ == '__main__':
    neihan = NeiHan()
    neihan.run()

"""
理解一下 BytesIO 和StringIO

很多时候，数据读写不一定是文件，也可以在内存中读写。
StringIO顾名思义就是在内存中读写str。
BytesIO 就是在内存中读写bytes类型的二进制数据

例子中如果使用StringIO 即f = StringIO(response.text)会产生"cannot identify image file"的错误
当然上述例子也可以把图片存到本地之后再使用Image打开来获取图片大小

"""
