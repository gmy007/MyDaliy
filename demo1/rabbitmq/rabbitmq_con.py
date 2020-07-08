# -*- coding: utf-8
import pika


class RabbitmqConnection(object):
    def __init__(self, username='guest', password='guest', host='127.0.0.1', virtual_host='/'):
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, virtual_host=virtual_host, credentials=self.credentials)
        )
        self.channel = self.connection.channel()

    def get_connection(self):
        return self.connection

    def get_channel(self):
        return self.channel
