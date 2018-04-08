# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

"""
定位元素的8种方法:
el = driver.find_element_by_id				使用id值定位
el = driver.find_elements_by_xpath			使用xpath定位
el = driver.find_elements_by_tag_name		使用标签名定位
el = driver.find_elements_by_link_text 		使用文本定位
el = driver.find_elements_by_partial_link_text 	使用部分文本定位
el = driver.find_elements_by_name 			使用name属性值定位
el = driver.find_elements_by_class_name 		使用class属性值定位
el = driver.find_elements_by_css_selector		使用css选择器定位
首选定位到ｉｆｒａｍｅ的ＸＰＡＴＨ然后继续ＸＰＡＴＨ操作
"""
options = Options()
# 如果想使用Headless Chrome 对Chrome版本有一定的要求，从官方文档我们可以看出，mac和linux环境要求chrome版本是59+，而windows版本的chrome要求是60+，同时chromedriver要求2.30+版本
options.add_argument('--headless')  # 无头参数
# 创建浏览器对象
driver = webdriver.Chrome(chrome_options=options)
# driver = webdriver.PhantomJS()
print(dir(driver))
# 发送请求，获取结果
wait = WebDriverWait(driver, timeout=10)
driver.get("http://www.baidu.com")
print("打开浏览器了！！")
html = driver.page_source  # 获取源码(是elements里面的源码不是network中的)
cookies = driver.get_cookies()  # 获取所有的cookie
driver.delete_cookie("name")  # 删除指定名字的cookie
driver.delete_all_cookies()  # 删除所有的cookie
current_url = driver.current_url  # 获取请求的url
title = driver.title  # 获取title标签的text
# driver.maximize_window() # 全屏操作
# 保存快照
driver.save_screenshot("baidu.jpg")
driver.get_screenshot_as_file("baidu2.png")
driver.get_screenshot_as_png()  # 直接保存为png
# res = driver.find_element_by_xpath("//div")
# 定位百度的搜索框 返回的element对象
more_ele = driver.find_elements_by_tag_name("a")
input_text = driver.find_element_by_id("kw")
input_text.send_keys("哈哈")
input_text.get_attribute("value")  # 元素获取属性
input_text.text  # 获取文本
input_text.submit()

ret1 = driver.find_element_by_link_text("新闻")
# 定位到包含指定字符的字符串,必须要有link
ret2 = driver.find_element_by_partial_link_text("hao")  # 注意如果有多个重复的包含值返回第一个因为是element
# 往指定的标签中填写字符串
input_text.send_keys("斗鱼")
# 定位搜索按钮
# submitBy = driver.find_element(By.XPATH("//a")) # 不经常使用
submit = driver.find_element_by_xpath("//input[@type='submit']")

submit.click()
input_text.clear()
input_text.send_keys("哈哈")
submit.click()
# 关闭浏览器
import time

time.sleep(10)
# 建议使用close()
driver.close()
# driver.quit()
