import http.client, mimetypes, urllib, json, time, requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image


######################################################################

class YDMHttp:
    apiurl = 'http://api.yundama.com/api.php'
    username = ''
    password = ''
    appid = ''
    appkey = ''

    def __init__(self, username, password, appid, appkey):
        self.username = username
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    def request(self, fields, files=[]):
        response = self.post_url(self.apiurl, fields, files)
        response = json.loads(response)
        return response

    def balance(self):
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001

    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if (cid > 0):
            for i in range(0, timeout):
                result = self.result(cid)
                if (result != ''):
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

    def report(self, cid):
        data = {'method': 'report', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'cid': str(cid), 'flag': '0'}
        response = self.request(data)
        if (response):
            return response['ret']
        else:
            return -9001

    def post_url(self, url, fields, files=[]):
        for key in files:
            files[key] = open(files[key], 'rb');
        res = requests.post(url, files=files, data=fields)
        return res.text


######################################################################

# 用户名
username = 'shengjun'

# 密码
password = '123+456shengjun'

# 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
appid = 1

# 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
appkey = '22cc5376925e9387a23cf797cb9ba745'  # 不需要改

# 图片文件
filename = 'captcha.jpg'

# 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
codetype = 3008

# 超时时间，秒
timeout = 60


def get_code():
    # 检查
    if (username == 'username'):
        print('请设置好相关参数再测试')
    else:
        # 初始化
        yundama = YDMHttp(username, password, appid, appkey)

        # 登陆云打码
        uid = yundama.login();
        print('uid: %s' % uid)

        # 查询余额
        balance = yundama.balance();
        print('balance: %s' % balance)

        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        cid, result = yundama.decode(filename, codetype, timeout);
        print('cid: %s, result: %s' % (cid, result))
        return result


######################################################################
#
# code = get_code()
# print("code:%s" % code)
def crawl():
    # 创建浏览器对象
    driver = webdriver.Chrome()
    # driver.maximize_window()
    driver.get("http://www.ipe.org.cn/IndustryRecord/Regulatory.aspx?keycode=343j9f9ri329293r3ri")
    time.sleep(10)
    all_company = driver.find_elements_by_xpath("//*[@id='table_con0']/div[2]/table//tr/td[2]")
    for item in all_company:
        print(item.text)
    all_city = driver.find_elements_by_xpath("//*[@id='table_con0']/div[2]/table//tr/td[3]")
    for item in all_city:
        print(item.text.strip())
    all_years = driver.find_elements_by_xpath('//*[@id="table_con0"]/div[2]/table//tr/td[4]')
    for item in all_years:
        print(item.text)
    all_count = driver.find_elements_by_xpath('//*[@id="table_con0"]/div[2]/table//tr/td[5]')
    for item in all_count:
        print(item.text)

    # 找到下一页
    xiayiye = driver.find_element_by_xpath("//*[@id='pagination0']/div/div/div[2]/input")
    xiayiye.clear()
    xiayiye.send_keys("2")
    # xiayiye = driver.find_element_by_class_name("icon icon-arrow-right-active")
    button = driver.find_element_by_xpath('//*[@id="pagination0"]/div/div/div[2]/button')
    button.click()
    pxd = 0
    driver.save_screenshot('screenshot.png')
    yanzhengma = driver.find_element_by_xpath('/html/body/div[last()]/div[2]/div[2]/div/div[1]/img')
    left = 578
    top = 270
    right = 650
    bottom = 320
    im = Image.open('screenshot.png')
    im = im.crop((left, top, right, bottom))
    im.save('captcha.jpg')
    # print(yanzhengma.get_attribute("src"))
    code = get_code()
    print("识别的验证码是%s" % code)
    driver.find_element_by_id("txtCode").send_keys(code)
    button_queren = driver.find_element_by_xpath('/html/body/div[last()]/div[2]/div[2]/div/div[2]/a')
    button_queren.click()
    while True:
        pass


if __name__ == '__main__':
    crawl()
