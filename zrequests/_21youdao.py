# -*- coding:utf-8 -*-

"""
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


class YouDao(object):
    def __init__(self):
        self.url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        self.file = open("youdao.json", "w", encoding="utf-8")
        # 定义发送post请求的参数,需要自己生成
        self.post_data = None

    def generate_post_param(self, word):
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
        salt = str(int(time.time() * 1000) + random.randint(0, 9))
        S = "fanyideskweb"
        temp = {
            "i": word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": "1523015870703",
            "sign": "db8d30ed12d1a1f1db6125aa9da17c60",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTIME",
            "typoResult": "false",

        }

    def run(self):
        pass


if __name__ == '__main__':
    y = YouDao()
    y.run()
