import pika
# '192.168.133.128'
credentials = pika.PlainCredentials('gmy', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.133.128', port=5672, virtual_host='/', credentials=credentials))

channel = connection.channel()
value = 'value_produce'
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = 'log.critical'
message = 'hello world'

channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)
channel.basic_publish(exchange='topic_logs', routing_key='alert.critical', body=message)
channel.basic_publish(exchange='topic_logs', routing_key='alert.critical', body='quit')
# 032604