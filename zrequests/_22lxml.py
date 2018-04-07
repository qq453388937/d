# -*- coding:utf-8 -*-
from lxml import etree
import requests


def myfunc():
    text = ''' <div> 
    <ul> 
    <li class="item-1"><a href="link1.html">first item</a></li> 
    <li class="item-1"><a href="link2.html">second item</a></li>
      <li class="item-inactive"><a href="link3.html">third item</a></li>
      <li class="item-1"><a href="link4.html">fourth item</a></li> 
      <li class="item-0"><a href="link5.html">fifth item</a> 
    # 注意，此处缺少一个 </li> 闭合标签 
   </ul>
   </div> '''
    # 使用etree 创建对象,把文本转换成elements对象
    html = etree.HTML(text)
    print(html)  # <Element html at 0x7fbc923b0d88>
    print(type(html))  # <class 'lxml.etree._Element'>
    print(dir(html))
    # 返回的是对象
    print(html.xpath("//div/ul/li[1]/a/@href"))
    # 提取文本返回的是列表,需要对提取的结果进行遍历,或者说再次XPATH
    # print(html.xpath("//div/ul/li/a/text()"))
    print(html.xpath("//div/ul/li")) # 外部xpath 内部再次遍历

    print(html.xpath("//div/ul/li/a")[0])


if __name__ == '__main__':
    myfunc()
