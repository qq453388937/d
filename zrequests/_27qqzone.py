# -*- coding:utf-8 -*-
import  time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
"""
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
为什么需要等待浏览器进行渲染内容过多网速的太慢这个时候就可以设置一个等待时间，强制要求在时间内出现，否则报错强制等待time.sleep(10)
显式等待显式等待指定某个条件，然后设置最长等待时间。如果在这个时间还没有找到元素，那么便会抛出异常了。
WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.ID, "myDynamicElement"))
隐式等待就是简单地设置一个最大等待时间，单位为秒。所有的元素定位操作都会使用该时间
driver.implicitly_wait(10)
"""

# 创建浏览器对象
driver = webdriver.Chrome()
url = "https://qzone.qq.com/"

driver.get(url)

# 切换导iframe里面
# 第一种
# iframe1 = driver.switch_to.frame("loginframe")# id进入
# driver.switch_to.frame(iframe1)

# 第二种
iframe = driver.find_element_by_xpath('//*[@id="login_frame"]')
driver.switch_to.frame(iframe)


# 获取尝试账号密码元素
button = driver.find_element_by_xpath('//*[@id="switcher_plogin"]')
button.click()
time.sleep(1)

# 账号
txt_name = driver.find_element_by_xpath('//*[@id="u"]')
txt_name.send_keys("643358477")
time.sleep(1)
# 密码
txt_pwd = driver.find_element_by_xpath('//*[@id="p"]')
txt_pwd.send_keys("qq2921481")
time.sleep(2)
# 登陆
denglu = driver.find_element_by_xpath('//*[@id="login_button"]')
denglu.click()
while True:
    pass
