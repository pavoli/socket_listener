# -*- coding: utf-8 -*-
import conf
import create_socket
from threading import Thread
import logging


logging.basicConfig(
    filename=conf.LOG_FILE_NAME,
    level=logging.DEBUG,
    format='%(asctime)s | %(message)s'
)


def run(port):
    s = create_socket.socket_server(conf.IP, port)
    s.create()


if __name__ == '__main__':
    for port in conf.PORTS:
        logging.info('{} | THREAD'.format(port))

        thread = Thread(target=run, args=(port,))
        thread.start()
        # thread.join()