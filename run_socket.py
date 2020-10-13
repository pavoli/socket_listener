# -*- coding: utf-8 -*-
from threading import Thread

import conf
import create_socket


def run(port):
    s = create_socket.socket_server(conf.IP, port)
    s.create()


if __name__ == '__main__':
    for port in conf.PORTS:
        create_socket.log.debug('{} | THREAD'.format(port))

        thread = Thread(target=run, args=(port,))
        thread.start()
