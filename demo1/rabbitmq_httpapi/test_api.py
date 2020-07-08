from rabbitmq.rabbitmq_con import RabbitmqConnection
import time



def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    if body == 'quit':
        ch.basic_cancel(consumer_tag='hello-consumer')
        ch.stop_consuming()


def consume():
    channel = RabbitmqConnection().get_channel()
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    Q1 = channel.queue_declare('test.api.Q1', exclusive=True)
    Q2 = channel.queue_declare('test.api.Q2', exclusive=True)
    channel.queue_bind(exchange='topic_logs', queue='test.api.Q1', routing_key='log.*')

    channel.queue_bind(exchange='topic_logs', queue='test.api.Q2', routing_key='*.critical')
    channel.basic_consume('test.api.Q1', callback, auto_ack=True)
    channel.basic_consume('test.api.Q2', callback, auto_ack=True)
    channel.start_consuming()


def produce():
    channel = RabbitmqConnection().get_channel()
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    routing_key = 'log.critical'
    message = 'hello world'

    channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
    channel.basic_publish(exchange='topic_logs', routing_key='log.critical', body=message)
    channel.basic_publish(exchange='topic_logs', routing_key='alert.critical', body='no quit')


if __name__ == '__main__':
    consume()
