import pika


def callback(ch, method, props, body):
    print '-'*30
    print method.routing_key
    print props.headers
    print body.decode()
    ch.basic_ack(delivery_tag=method.delivery_tag)


def fun():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672,
                                                                   virtual_host='/', credentials=credentials))
    channel = connection.channel()
    queue = channel.queue_declare(queue='trace_queue')
    channel.queue_bind(exchange='amq.rabbitmq.trace', queue='trace_queue', routing_key='publish.#')
    channel.basic_consume(queue='trace_queue', on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    fun()
