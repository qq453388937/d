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


driver.get("http://www.douyu.com")
print("浏览器打开了")