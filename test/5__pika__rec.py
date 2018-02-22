# -*- coding:utf-8 -*-
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='helloQueue')


def callback(ch, method, properties, body):
    print(" [>>>]Receive %r" % body)


channel.basic_consume(callback, queue='helloQueue', no_ack=True)
print(' [*] Waitting for message. To exit press CTRL+C')
channel.start_consuming() # 获取队列中的信息