# -*- coding:utf-8 -*-
import sys, requests, json


class King(object):
    def __init__(self, word):
        self.url = 'http://fy.iciba.com/ajax.php?a=fy'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }

        self.params = {
            "f": "auto",
            "t": "auto",
            "w": word,
        }

    def parse_data(self, data):
        dict_data = json.loads(data)
        if 'out' in data:
            content = (dict_data['content']['out'])
        else:
            content = (dict_data['content']['word_mean'][0])
        print(content)

    def request_post(self):
        response = requests.post(url=self.url, headers=self.headers, data=self.params)
        # return response.text
        return response.content.decode()  # 解码后的文字 utf-8

    def run(self):
        data = self.request_post()
        # 调用解析的方法
        self.parse_data(data)


if __name__ == '__main__':
    import sys

    word = sys.argv[1]
    king = King(word)
    king.run()
