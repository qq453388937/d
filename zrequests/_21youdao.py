# -*- coding:utf-8 -*-

"""
数据格式
i:gold
from:AUTO
to:AUTO
smartresult:dict
client:fanyideskweb
salt:1523015870703
sign:db8d30ed12d1a1f1db6125aa9da17c60
doctype:json
version:2.1
keyfrom:fanyi.web
action:FY_BY_REALTIME
typoResult:false

"""
import hashlib
import requests
import json


class YouDao(object):
    def __init__(self):
        self.url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Cookie": "OUTFOX_SEARCH_USER_ID=-97501377@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=165541613.55608284; JSESSIONID=aaaPCFjf3NRx27CVKBDkw; ___rl__test__cookies=1523061676655",
            "Host": "fanyi.youdao.com",
            "Origin": "http://fanyi.youdao.com",
            "Referer": "http://fanyi.youdao.com/"
        }
        self.file = open("youdao.json", "w", encoding="utf-8")
        # 定义发送post请求的参数,需要自己生成
        self.post_data = None

    def generate_post_param(self, word):
        """生成post请求的参数return回去"""
        # 生成时间戳和一个0到9的随机数进行相加(13位)
        """
        var n = b.val()
          , r = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10))
          , o = u.md5(S + n + r + D)
          , a = n.length;
        """
        # r ===> salt
        # S ===> S = "fanyideskweb"  line 8546
        import time, random
        # random.randint(0,9) 随机[1,9] 和时间戳组合
        salt = str(int(time.time() * 1000) + random.randint(0, 9))  # 模仿有道生成
        print(salt)
        S = "fanyideskweb"
        D = "ebSeFb%=XZ%T[KZ)c(sy!"
        temp_str = S + word + salt + D
        hashmy = hashlib.md5()
        hashmy.update(temp_str.encode())  # b'' update的参数
        o = hashmy.hexdigest()
        print(o)
        temp = {
            "i": word,  # 传入word
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": o,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTIME",
            "typoResult": "false",
        }
        return temp

    def get_data(self, data):
        params_dict = self.generate_post_param(data)
        response = requests.post(self.url, headers=self.headers, data=params_dict)
        return response.content.decode()

    def parse_data(self, json_str):
        my_dict = json.loads(json_str)
        temp_dict = dict()
        translateResult = my_dict["translateResult"][0][0]
        temp_dict["tgt"] = translateResult["tgt"]
        temp_dict["src"] = translateResult["src"]
        return temp_dict

    def save_data(self, data_dict):
        self.file.write(json.dumps(data_dict,ensure_ascii=False) + ",\n")

    def __del__(self):
        self.file.close()

    def run(self):
        content = self.get_data("人生苦短")
        data_dict = self.parse_data(content)
        self.save_data(data_dict)
        print(content)


if __name__ == '__main__':
    y = YouDao()
    y.run()
