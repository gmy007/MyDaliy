# -*- coding:utf-8 -*-
import json
import pprint
import requests
from models import ConsumerConnection, ConsumerService
from mongoengine import connect


def get_consumer_msg():
    return requests.get(url='http://192.168.229.153:15682/api/consumers',
                        auth=('guest', 'guest')).content


def get_binding_msg():
    return requests.get(url='http://192.168.229.153:15682/api/bindings',
                        auth=('guest', 'guest')).content


def log_parser(log_str):
    if log_str is None:
        print 'str cant be None'
        return
    part_of_str = log_str.partition(',')
    if part_of_str[0].find('[exchange][create]') == -1:
        raise ValueError
    if part_of_str[2].find('exchange') == -1 or part_of_str[2].find('conn') == -1:
        raise ValueError
    str_dict = json.loads(part_of_str[2])
    str_dict['conn'] = str_dict['conn'].partition(' -> ')[0]
    return str_dict


def consumers_q2c_parser(consumer_msg):
    '''
    通过httpApi得到consumer原始信息，解析出channel和queue的关系集合
    :param consumer_msg:
    :return: dict：{queue:[conn]}
    '''
    consumer_dict = json.loads(consumer_msg)
    ret = {}
    for i in consumer_dict:
        conn = i['channel_details']['peer_host'] + ':' + str(i['channel_details']['peer_port'])
        queue = i['queue']['name']
        if queue not in ret.keys():
            ret[queue] = []
        ret[queue].append(conn)
    return ret


def consumers_c2q_parser(consumer_msg):
    '''
    通过httpApi得到consumer原始信息，解析出channel和queue的关系集合
    :param consumer_msg:
    :return: dict：{conn:[queue]}
    '''
    consumer_dict = json.loads(consumer_msg)
    ret = {}
    for i in consumer_dict:
        conn = i['channel_details']['peer_host'] + ':' + str(i['channel_details']['peer_port'])
        queue = i['queue']['name']
        if conn not in ret.keys():
            ret[conn] = []
        ret[conn].append(queue)
    return ret


def bindings_api_parser(bindings_msg):
    '''
    通过httpApi得到的bindings原始信息，解析exchange和queue的关系集合
    :param bindings_msg:
    :return: {exchange_name:[queue]}
    '''
    bindings_dict = json.loads(bindings_msg)
    ret = {}
    for binding in bindings_dict:
        exchange_name = binding['source']
        if len(exchange_name) == 0:
            continue
        if exchange_name not in ret.keys():
            ret[exchange_name] = {}
        if binding['destination_type'] == 'queue':
            # ret[exchange_name].append({binding['destination']: binding['routing_key']})
            ret[exchange_name][binding['destination']] = binding['routing_key']
    return ret


def get_service(ip):
    return ''


'''
connection [{ip:ip,port:port,service:service,routing_key:key},]
'''


def parser():
    '''
    得到初步解析好的bindings和consumer信息，解析出exchange和service对应关系
    :return: [{'exchange_name':value,'connection':[{'ip':value,'port':value,'service':value}]}]
    '''
    consumer_ret = consumers_q2c_parser(get_consumer_msg())
    print consumer_ret
    bindings_ret = bindings_api_parser(get_binding_msg())
    print bindings_ret
    result = []
    for exchange, v in bindings_ret.items():
        cur = {}
        cur['exchange_name'] = exchange
        con = []
        for queue_name, r in v.items():
            if queue_name not in consumer_ret.keys():
                continue
            con_name = consumer_ret[queue_name]
            for ip in con_name:
                service = {}
                service['ip'] = ip
                service['service'] = get_service()
                service['routing_key'] = r
                if not check_conn(con, service):
                    con.append(service)
        cur['connection'] = con
        result.append(cur)
    print result
    return result


def check_conn(con_list, service):
    '''
    判断当前得到的一组connection数据是否与exchange别的connection数据重复
    :param con_list:
    :param service:
    :return: bool
    '''
    for conn in con_list:
        if conn['ip'] == service['ip'] and conn['service'] == service['service'] \
                and conn['routing_key'] == service['routing_key']:
            return True
    return False


def mongoDB_save():
    '''
    最后解析出的数据存入mongoDB
    :return:
    '''
    connect('pytest', host='127.0.0.1', port=27017)
    parser_ret = parser()
    for i in parser_ret:
        conn = i['connection']
        con_service = ConsumerService(exchange_name=i['exchange_name'], connection=[])
        for j in conn:
            # consumer_con = ConsumerConnection(ip=j['ip'],
            #                   routing_key=j['routing_key'], service=j['service'])
            consumer_con = {}
            ip_part = j['ip'].partition(':')
            consumer_con['ip'] = ip_part[0]
            consumer_con['port'] = int(ip_part[2])
            consumer_con['routing_key'] = j['routing_key']
            consumer_con['service'] = j['service']
            con_service.connection.append(consumer_con)
        con_service.save()


def judge_service(consumer_msg):
    pass


def strategy_parser():
    consumer_ret = consumers_q2c_parser(get_consumer_msg())
    print consumer_ret
    bindings_ret = bindings_api_parser(get_binding_msg())
    print bindings_ret
    result = []
    for exchange, v in bindings_ret.items():
        cur = {}
        cur['exchange_name'] = exchange
        cur_strategy = get_strategy(v, consumer_ret)
        cur['service'] = cur_strategy
        result.append(cur)
    return result


def get_strategy(queue_list, consumer_ret):
    '''
    通过得到的当前exchange对应的队列集合和所有消费者信息，
    来获取当前exchange上服务对应的策略
    :param queue_list:当前exchange对应所有queue
    :param consumer_ret:所有consumer信息
    :return: list：[{service_name:value, strategy:value}]
    '''
    if len(queue_list) == 0:
        return []
    ret = []
    all_channel = []
    exclusive_channel = []
    for queue_name in queue_list:
        if queue_name in consumer_ret.keys():
            exclusive_channel = consumer_ret[queue_name]
            break
    for queue_name in queue_list:
        if queue_name not in consumer_ret.keys():
            continue
        conn_list = consumer_ret[queue_name]
        all_channel = list(set(all_channel).union(set(conn_list)))
        for conn in exclusive_channel:
            if conn not in conn_list:
                exclusive_channel.remove(conn)
    # print all_channel
    # print exclusive_channel
    cur_dict = {}
    for channel in all_channel:
        service = get_service(channel)
        if service in cur_dict.keys() and cur_dict[service] == 'Exclusive':
            continue
        if channel in exclusive_channel:
            cur_dict[service] = 'Exclusive'
        else:
            cur_dict[service] = 'Share'
    for k, v in cur_dict.items():
        cur = {}
        cur['service_name'] = k
        cur['strategy'] = v
        ret.append(cur)
    return ret


if __name__ == '__main__':
    # mongoDB_save()
    # pprint.pprint(consumers_api_c2q_parser(get_consumer_msg()))
    # consumer_c2q_msg = consumers_c2q_parser(get_consumer_msg())
    # judge_service(consumer_c2q_msg)
    # parser()
    strategy_parser()
