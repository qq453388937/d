# -*- coding:utf-8 -*-

data  = '北京_python24'
print(data)
print(type(data))

# 编码成bytes
data_bytes = data.encode()
print(data_bytes)
print(type(data_bytes))

# 解码成str
data_str = data_bytes.decode()
print(data_str)
print(type(data_str))
