# -*- coding:utf-8 -*-
from nameko.events import EventDispatcher, event_handler
from nameko.rpc import rpc, RpcProxy

CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}


class ServiceY:
    name = "service_y"

    @rpc
    def append_identifier(self, value):
        return u"{}-y".format(value)


class ServiceX:
    name = "service_x"

    y = RpcProxy("service_y")

    @rpc
    def remote_method(self, value):
        res = u"{}-x".format(value)
        return self.y.append_identifier(res)


class ServiceA:
    """ Event dispatching service. """
    name = "service_a"

    dispatch = EventDispatcher()

    @rpc
    def dispatching_method(self, payload):
        self.dispatch("event_type", payload)


class ServiceB:
    """ Event listening service. """
    name = "service_b"

    @event_handler("service_a", "event_type")
    def handle_event(self, payload):
        print "service b received:" + payload
