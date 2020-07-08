# -*- coding: utf-8
import test_api
import requests
import json
from rabbitmq.rabbitmq_con import RabbitmqConnection


def produce():
    channel = RabbitmqConnection().get_channel()
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    routing_key = 'log.critical'
    message = 'hello world'
    # 所有message都会发布到默认exchange 通过路由键=队列名  来发布信息
    # channel.basic_publish(exchange='', routing_key='test.api.Q1', body='default message')
    channel.basic_publish(exchange='topic_logs', routing_key='log.critical', body=message)
    channel.basic_publish(exchange='topic_logs', routing_key='alert.critical', body='no quit')


if __name__ == '__main__':
    # test_api.produce()
    produce()
    res = requests.get(url='http://192.168.229.153:15682/api/consumers', auth=('guest', 'guest'))
    print(json.loads(res.content.decode()))
    res = requests.get(url='http://192.168.229.153:15682/api/bindings', auth=('guest', 'guest'))
    # print type(res.content)
    print(json.loads(res.content.decode()))
