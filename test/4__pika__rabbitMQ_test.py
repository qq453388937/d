# -*- coding:utf-8 -*-
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 创建信道 AMQP协议规定通过channel才能执行AMQP命令 一个connection可以包含多个信道
# 官方建议用connection 串行发送消息,不要共用channel
channel.queue_declare(queue='helloQueue')  # 声明一个队列
channel.basic_publish(exchange='', routing_key='helloQueue', body='[A001]Hello my rabbitMQ world ')
print(" [10001] Sent 'Hello my rabbitMQ world'")
connection.close()
