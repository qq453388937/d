# -*- coding:utf-8 -*-

import requests


def func1():
    url = "https://www.baidu.com/s?"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }

    data = {
        "wd": "python"
    }

    response = requests.get(url, headers=headers, params=data)

    print(response.status_code)
    print(response.text)


def func2():
    url = 'http://www.zhihu.com/'

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    print(response.status_code)


if __name__ == '__main__':
    func2()
