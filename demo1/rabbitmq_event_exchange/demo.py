# -*- coding: utf-8
import pika


def callback(ch, method, props, body):
    print '*' * 20 + ' Call back ' + '*' * 20
    print method.routing_key
    print props.headers
    print
    ch.basic_ack(delivery_tag=method.delivery_tag)


credentials = pika.PlainCredentials('guest', 'guest')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()

con_queue = channel.queue_declare(queue='connection_msg')
exc_queue = channel.queue_declare(queue='exchange_msg')
exc_queue = channel.queue_declare(queue='binding_msg')
channel.queue_bind(exchange='amq.rabbitmq.event', queue='exchange_msg', routing_key='exchange.*')
# channel.queue_bind(exchange='amq.rabbitmq.event', queue='connection_msg', routing_key='connection.*')
# channel.queue_bind(exchange='amq.rabbitmq.event', queue='binding_msg', routing_key='binding.*')
channel.basic_consume(queue='exchange_msg', on_message_callback=callback)
# channel.basic_consume(queue='connection_msg', on_message_callback=callback)
# channel.basic_consume(queue='binding_msg', on_message_callback=callback)
channel.start_consuming()
