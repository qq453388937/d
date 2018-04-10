# -*- coding:utf-8 -*-
"""
XPath	JSONPath	描述
/	$	根节点
.	@	现行节点
/	.or[]	取子节点
..	n/a	取父节点，Jsonpath未支持
//	..	就是不管位置，选择所有符合条件的条件
*	*	匹配所有元素节点
@	n/a	根据属性访问，Json不支持，因为Json是个Key-value递归结构，不需要。
[]	[]	迭代器标示（可以在里边做简单的迭代操作，如数组下标，根据内容选值等）
|	[,]	支持迭代器中做多选。
[]	?()	支持过滤操作.
n/a	()	支持表达式计算
()	n/a	分组，JsonPath不支持
"""

import requests
import json
import jsonpath

response = requests.get("http://www.lagou.com/lbs/getAllCitySearchLabels.json")
# print(response.content.decode())
json_str = response.content.decode()

json_str_str = """{ "store": {
    "book": [ 
      { "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      { "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 12.99
      },
      { "category": "fiction",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 8.99
      },
      { "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  }
} """  # 转换为字典对象
my_dict = json.loads(json_str)
city_name_list = jsonpath.jsonpath(my_dict, '$..code,name')  # 这个节点很实用
city_name_list = jsonpath.jsonpath(my_dict, '$.content.data.allCitySearchLabels')  # 这个节点很实用
city_name_list = jsonpath.jsonpath(my_dict, '$..A[*]')  # [*] 可以把[[{},{}]] => [{},{}]转换成标准的
city_name_list = jsonpath.jsonpath(city_name_list, "$..[?(@.id==601)]")  # nice
my_dict_dict = json.loads(json_str_str)  # 网站上的json
# 必须是[{},{},{}]
test_list1 = jsonpath.jsonpath(my_dict_dict, '$..book[?(@.price<10)]')
# [{}]列表嵌套字典中找出包含isbn键的 {} 字典
test_list1 = jsonpath.jsonpath(my_dict_dict, "$..book[?(@.isbn)]")
# 注意[*] 把[[{},{}]] 转换成[{},{}]
test_list1 = jsonpath.jsonpath(my_dict_dict, "$.store.book[*].author")


# print(my_dict)
# print(type(my_dict))
# print(city_name_list)  # ['郑州', '珠海', '中山', '肇庆', ...]

print(test_list1)
# print(test_list1)
