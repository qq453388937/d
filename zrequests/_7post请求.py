# -*- coding:utf-8 -*-
import requests


class Jinshan(object):

    def __init__(self):
        self.url = "http://fy.iciba.com/ajax.php?a=fy"
        self.hearders = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        self.post_data = {
            "f": "auto",
            "t": "auto",
            "w": "Life is short, short, short, short, short"
        }

    def request_post(self):
        response = requests.post(url=self.url, data=self.post_data, headers=self.hearders)
        # print(response.content.decode())
        return response.content.decode()

    def parse_json(self, data):
        import json
        my_dict = json.loads(data)
        if "out" in data:
            print(my_dict["content"]["out"])
        else:
            print(my_dict["content"]["word_mean"][0])

    def run(self):
        data = self.request_post()
        dict_my = self.parse_json(data)


if __name__ == '__main__':
    j = Jinshan()
    j.run()
