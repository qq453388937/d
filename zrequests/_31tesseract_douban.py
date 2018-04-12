# -*- coding:utf-8 -*-
from selenium import webdriver
import pytesseract
from PIL import Image
import requests
import time
from selenium.webdriver.chrome.options import Options


options = Options()
# 如果想使用Headless Chrome 对Chrome版本有一定的要求，从官方文档我们可以看出，mac和linux环境要求chrome版本是59+，而windows版本的chrome要求是60+，同时chromedriver要求2.30+版本
options.add_argument('--headless')

# 创建浏览器对象
driver = webdriver.Chrome(chrome_options=options)

# 发送请求
driver.get("https://accounts.douban.com/login")
print("打开浏览器了！！")
# 定位元素帐号
ele_email = driver.find_element_by_id("email")
# 把账号发送给表单
ele_email.send_keys("371673381@qq.com")
print(ele_email.get_attribute("value"))
# 定位密码元素
ele_pswd = driver.find_element_by_id("password")
# 把密码发送给表单
ele_pswd.send_keys("123456shengjun")
print(ele_pswd.get_attribute("value"))

# # 验证码
# ele_image_captcha = driver.find_element_by_id("captcha_image")
# image_url = ele_image_captcha.get_attribute("src")
# print(image_url)
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
#
# }
#
# img = Image.open('douban.jpg')
# image_str = pytesseract.image_to_string(img)
# print('-------', image_str, '-------')

# 定位登录按钮
ele_submit = driver.find_element_by_name('login')
# 模拟点击
ele_submit.click()

print("登录了")
