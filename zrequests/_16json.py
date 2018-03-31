# -*- coding:utf-8 -*-
import json

# json 字符串用双引号
dict_data = '{"itacast": "北京24","name":"dict_data"}'
err_data = "{'itcast':'北京24','name':'err_data'}"  # 注意json字符串必须是双引号!!!!!!!
my_dict = {"itacast": "北京24", "name": "my_dict"}

# 默认使用ascii编码 ,设置ascii编码为false
json_data = json.dumps(my_dict, ensure_ascii=False)
print(json_data)
print(type(json_data))

json_data = json.loads(json_data)
print(json_data)
print(type(json_data))
# 第一个参数是字典，第二个参数是file对象，第三个参数是编码｀｀｀
with open("data.json", "w", encoding="utf8") as f:
    # 把字典转换成ｊｓｏｎ写入文件   json.dump()
    json.dump(json_data, f, ensure_ascii=False)

# 写文件时如果遇到编码错误 ,可以指定编码格式为utf-8
with open("data.json", "r", encoding="utf8") as f:
    json_data = json.load(f)
    print(json_data)
    print(type(json_data))

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(my_dict, f, ensure_ascii=False)

with open("data.json", "r", encoding="utf-8") as f:
    ret = json.load(f)
    print(ret)
