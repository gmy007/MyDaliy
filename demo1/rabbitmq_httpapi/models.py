from mongoengine import *


class ConsumerConnection(Document):
    ip = StringField(max_length=256, required=True)
    port = IntField()
    service = StringField(max_length=1024)
    routing_key = StringField(max_length=1024)


class ConsumerService(Document):
    exchange_name = StringField(max_length=512, required=True, unique=True)
    connection = ListField(DictField())


class ConsumerStrategy(Document):
    exchange_name = StringField(max_length=512, required=True, unique=True)
    service = StringField(max_length=512)
    strategy = StringField(max_length=256)
