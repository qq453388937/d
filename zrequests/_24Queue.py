# -*- coding:utf-8 -*-
import threading
from queue import Queue
class Person(object):
    pass

q = Queue(1)  # 创建队列,兵可以指定大小

print(q.empty())  # 判断队列是否为空

print(q.full())  # 判断队列是否为满
#
q.put(Person())  # 向队列中放入数据
#
print(q.empty())  # 判断队列是否为空

print(q.full())  # 判断队列是否为满
ret = q.get()  # 从队列中取出数据
print(ret)

# q.task_done() # 宣告队列操作结束,并且修改队列状态
q.join() # 让主线程等待所有队列操作完毕后再结束
def func():
    pass

t = threading.Thread(target=func)
#  ['di:mən]
t.setDaemon(True) # 设置为守护进程,该线程会跟随主线程的退出而退出
