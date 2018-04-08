# -*- coding:utf-8 -*-
import sys
from lxml import etree
from queue import Queue
import json
import threading
import requests


class Qiushibaike(object):
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.url_list = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        self.file = open("qiushi.json", "w")
        # 创建3个队列对象

        self.url_queue = Queue()
        self.response_queue = Queue()
        self.data_queue = Queue()

    def generate_url_list(self):
        for i in range(1, 14):
            self.url_queue.put(self.url.format(i))

    def get_data(self):
        while True:
            # 获取队列中的url
            url = self.url_queue.get()
            print("正在获取{}的响应".format(url))
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 503:
                self.url_queue.put(url)  # 放回队列
            else:
                #  往队列中添加数据
                self.response_queue.put(response.content)
            self.url_queue.task_done()# 宣告队列结束,并且修改状态

    def parse_data(self):
        while True:
            data = self.response_queue.get()
            print("正在解析数据")
            # 创建elements对象
            html = etree.HTML(data)
            # 定位出帖子节点列表
            node_list = html.xpath("//*[contains(@id,'qiushi_tag_')]")
            #  print len(node_list)
            # 购进存放返回数据的列表

            data_list = []

            # 遍历节点列表,从每一个节点中抽取数据
            for node in node_list:
                temp = dict()
                try:
                    temp["user"] = node.xpath("./div[1]/a[2]/h2/text()")[0].strip()
                    temp["link"] = "http://www.qiushibaike.com" + node.xpath("./div[1]/a[2]/@href")[0]
                    temp["age"] = node.xpath("./div[1]/div/text()")[0]
                    temp["gender"] = node.xpath("./div[1]/div/@class").split(' ')[-1].replace("Icon", '')
                except:
                    temp["user"] = "匿名用户"
                    temp["link"] = None
                    temp["age"] = None
                    temp["gender"] = None
                # 将数据加入数据列表
                data_list.append(temp)

            self.data_queue.put(data_list)  # 最终的列表放入队列
            self.response_queue.task_done() # 宣告队列结束,并且修改状态

    def save_data(self):
        while True:
            data_list = self.data_queue.get()
            print("正在保存数据")
            for data in data_list:
                print(data)
                str_data = json.dumps(data) + ",\n"
                self.file.write(str_data)

            self.data_queue.task_done() # 宣告队列结束,并且修改状态

    def __del__(self):
        self.file.close()

    def run(self):
        # 创建线程列表
        thread_list = []
        # 创建生成url的线程
        t_generate_url = threading.Thread(target=self.generate_url_list)
        thread_list.append(t_generate_url)

        # 创建获取数据的线程
        for i in range(3):
            t = threading.Thread(target=self.get_data)
            thread_list.append(t)

        # 创建解析数据的线程
        for i in range(3):
            t = threading.Thread(target=self.parse_data)
            thread_list.append(t)

        # 开启线程
        for t in thread_list:
            t.setDaemon(True)
            t.start()

        # 关闭队列
        for q in [self.url_queue,self.response_queue,self.data_queue]:
            # 让主线程等待所有队列技术再退出
            q.join()

if __name__ == '__main__':
    q = Qiushibaike()
    q.run()