# -*- coding:utf-8 -*-
from nameko.standalone.rpc import ClusterRpcProxy

CONFIG = {
    'AMQP_URI': "amqp://guest:guest@127.0.0.1"  # e.g. "pyamqp://guest:guest@localhost"
}


def compute():
    # 获取RPC代理对象
    with ClusterRpcProxy(CONFIG) as cluster_rpc:
        cluster_rpc.hello_service.hello()  # 调用rpc服务


def rpc_config():
    with ClusterRpcProxy(CONFIG) as cluster_rpc:
        print cluster_rpc.service_x.remote_method("hello")


if __name__ == '__main__':
    with ClusterRpcProxy(CONFIG) as cluster_rpc:
        print cluster_rpc.service_a.dispatching_method('message')

