# -*- coding:utf-8 -*-

class E:
    # 经典类
    pass


class E1(object):
    # 新式类
    pass


e = E()
print
"经典类"
print(e)
print(type(e))
print(e.__class__)

print("新式类")
e1 = E1()
print(e1)
print(e1.__class__)
print(type(e1))
