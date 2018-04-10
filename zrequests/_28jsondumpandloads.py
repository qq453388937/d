# -*- coding:utf-8 -*-
import sys
import json

listStr = [{"city": "北京"}, {"name": "大刘"}]
json.dump(listStr, open("listStr.json", "w"), ensure_ascii=False)

dictStr = {"city": "北京", "name": "大刘"}
json.dump(dictStr, open("dictStr.json", "w"), ensure_ascii=False)

# json_load.py

import json

strList = json.load(open("listStr.json"))
print(strList)

# [{u'city': u'\u5317\u4eac'}, {u'name': u'\u5927\u5218'}]

strDict = json.load(open("dictStr.json"))
print(strDict)
# {u'city': u'\u5317\u4eac', u'name': u'\u5927\u5218'}
