import pika


def callback(ch, method, props, body):
    print method.routing_key
    print props.headers
    ch.basic_ack(delivery_tag=method.delivery_tag)


def fun():
    credentials = pika.PlainCredentials('gmy', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.133.128', port=5672,
                                                                   virtual_host='/', credentials=credentials))
    channel = connection.channel()
    queue = channel.queue_declare(queue='event_queue')
    channel.queue_bind(exchange='amq.rabbitmq.event', queue='event_queue', routing_key='exchange.*')
    channel.basic_consume(queue='event_queue', on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    fun()
