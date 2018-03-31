# -*- coding:utf-8 -*-
import re
"""
结构化数据: json xml 等
非结构化数据: html 文本
"""

data = 'python24,pypyppy'

print(re.findall('py', data))

data2 = "a\nb"
print(data2)
print(re.findall('a.b', data2, re.DOTALL, re.I))
print(re.findall("a.b", data2, re.S))

print(re.findall("a\nb", data2))

# 注意书写正则表达式时，原始字符串是什么，正则表达式就什么，不同平台换行符号不一样

demo = "itcast/python"

print(re.findall("t|p", demo))

demo2 = "cadawd12332dawd134213"

# print(re.findall(r"\d", demo2))
print(re.findall(r"\d+", demo2))
print(re.findall(r"\d+?", demo2))  # 非贪婪最少匹配一个数字

par = re.compile("\d")  # 正则表达式对象 return a pattern object  编译一个正则对象

data = par.findall(demo2)
