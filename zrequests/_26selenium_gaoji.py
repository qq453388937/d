# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

options = Options()
# 如果想使用Headless Chrome 对Chrome版本有一定的要求，从官方文档我们可以看出，mac和linux环境要求chrome版本是59+，而windows版本的chrome要求是60+，同时chromedriver要求2.30+版本
options.add_argument('--headless')  # 无头参数

# 创建浏览器对象
driver = webdriver.Chrome(chrome_options=options)

driver.get("http://bj.58.com/")
a = driver.find_element_by_xpath("//a[@href='/house.shtml']")
a.click()

ret = driver.window_handles # 这玩意是个列表字符串,取最后一个就是第二个窗口的name
# driver.switch_to_window() # 旧的方法
driver.switch_to.window(driver.window_handles[-1])
driver.get_screenshot_as_file("58.png")

els = driver.find_elements_by_xpath("//a")
for node in els:
    print(node.text,node.get_attribute("href"))


