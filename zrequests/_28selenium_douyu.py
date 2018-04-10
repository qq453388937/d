# -*- coding:utf-8 -*-
import time, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


class Douyu(object):
    def __init__(self):
        self.url = "https://www.douyu.com/directory/all"
        # 实例化浏览器对象
        self.driver = webdriver.Chrome()
        self.file = open("douyu.json", "w", encoding="utf-8")

    def parse_data(self):
        node_list = self.driver.find_elements_by_xpath("//*[@id='live-list-contentbox']/li/a")
        print(len(node_list))
        data_list = []
        for node in node_list:
            data = dict()
            # 存储属性
            data["title"] = node.find_element_by_xpath("./div/div/h3").text
            data["catagory"] = node.find_element_by_xpath("./div/div/span").text
            data["owner"] = node.find_element_by_xpath("./div/p/span[1]").text
            data["num"] = node.find_element_by_xpath("./div/p/span[2]").text
            data["url"] = node.find_element_by_xpath("./span/img").get_attribute("data-original")
            # data["link"] = node.get_attribute("href")
            print(data)
            data_list.append(data)
        return data_list

    def save_data(self, data_list):
        for data in data_list:
            self.file.write(json.dumps(data, ensure_ascii=False) + ",\n")
        print("写入成功")

    def __del__(self):
        self.driver.close()

    import time
    def run(self):
        # 构造url
        # 构造webdriver
        # 发送请求
        self.driver.get(self.url)
        while True:
            # 解析数据
            data_list = self.parse_data()
            # 保存数据
            self.save_data(data_list)
            # 点击下一页
            try:
                time.sleep(1)
                ele_next_url = self.driver.find_element_by_xpath("//*[class='shark-pager-next']")
                ele_next_url.click()
            except Exception as e:
                break


if __name__ == '__main__':
    d = Douyu()
    d.run()
