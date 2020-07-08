# -*- coding: utf-8
import pika

credentials = pika.PlainCredentials('guest', 'guest')

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='192.168.133.128', port=5672, virtual_host='/', credentials=credentials))

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()
value = 'value'
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# Q1 = channel.queue_declare('Q1', exclusive=True)
# Q2 = channel.queue_declare('Q2', exclusive=True)

# channel.queue_bind(exchange='topic_logs', queue='Q1', routing_key='log.*')
# channel.queue_bind(exchange='topic_logs', queue='Q2', routing_key='*.critical')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    if body == 'quit':
        channel.basic_cancel(consumer_tag='hello-consumer')
        channel.stop_consuming()


channel.basic_consume('test.api.Q1', callback, auto_ack=True)

# 此处打开了自动确定，无需再回调函数中设置
# ch.basic_ack(delivery_tag=method.delivery_tag)
# channel.basic_consume('Q2', callback, auto_ack=True)

channel.start_consuming()
