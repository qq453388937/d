import requests
import re

url = 'http://www.renren.com/PLogin.do'  # 表单例的action

# 保存cookie信息
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}

# 构造session回话对象
session = requests.session()

# 构造post请求data数据
data = {
    'email': '18949599846',  # form表单中name属性
    'password': 'shengjun'  # form表单中name属性
    #'_csrf':'token'
}
# 发送post请求
session.post(url, headers=headers, data=data)

# 验证登录是否成功 session.get
response = session.get('http://www.renren.com/963112933')

print(re.findall('风雨', response.content.decode()))
print(response.status_code)
