# -*- coding:utf-8
import logging
import sys
import time
import mainModule

logger = logging.getLogger(__name__)
log_file = 'log.txt'
now = time.strftime('%Y-%m-%d-%H-%M-%S')


def fun1():
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(
        stream=sys.stdout, level=logging.DEBUG,
        format='%(asctime)s %(name)s  %(levelname)-8s: %(message)s', filename=log_file)
    # 同时指定filename和stream参数，stream被忽略 不会打印控制台
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)
    logger.warning('123')
    logger.info("Start print log")
    logger.debug("Do something")
    logger.warning("Something maybe fail.")
    logger.info("Finish")


def fun2():
    logger2 = logging.getLogger(__name__)
    logger2.setLevel(level=logging.INFO)

    fileHandler = logging.FileHandler('log.txt')
    fileHandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)s  %(levelname)-8s: %(message)s')
    fileHandler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    logger2.addHandler(fileHandler)
    logger2.addHandler(console)
    logger2.info("Start print log")
    logger2.debug("Do something")
    logger2.warning("Something maybe fail.")

    try:
        raise Exception
    except Exception:
        # logger2.error('There are some Exceptions ', exc_info=True)
        logger2.exception('Message for log:  There are some Exceptions ')
    logger2.info("Finish")


def fun3():
    sublogger = logging.getLogger('mainModule.sub')
    sublogger.info('This is sub logger')
    str =[]
    sublogger.warning('用户输入信息有误：%s',type(str))


if __name__ == '__main__':
    # fun1()
    # fun2()
    fun3()
