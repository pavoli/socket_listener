# -*- coding: utf-8 -*-
__author__ = 'p.olifer'

import socket

import work_with_DB
import conf


def get_logger(name=__file__, file='log/log_{0}.txt', encoding='utf-8'):
    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # in file
    from logging import FileHandler
    from datetime import datetime
    
    now = datetime.now()
    fh = FileHandler(filename=file.format(now.strftime('%Y%m%d')), encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    # in stdout
    import sys
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


log = get_logger()


class socket_server():
    def __init__(self, ip, port):

        # self.ip = socket.gethostbyname(socket.gethostname())
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.debug('{0} | create socket'.format(self.port))

        self.sock.bind((self.ip, self.port))
        log.debug('{0} | bind to socket'.format(self.port))

        self.sock.listen(5)
        log.debug('{0} | listen socket'.format(self.port))

    def create(self):
        while True:
            self.conn, self.addr = self.sock.accept()
            log.debug('{0} | accept connection'.format(self.port))
            self.conn.setblocking(1)

            while True:
                try:
                    self.query_from_MES = self.conn.recv(10000).strip().decode('utf-8')

                    if not len(self.query_from_MES) == 0:
                        log.debug('{0} | receive data    | {1}'.format(self.port,
                                                                     self.query_from_MES))
                        flag = self.query_from_MES[0:3]
                        log.debug(
                            '{0} | flag            | {1}'.format(self.port, flag))

                        if flag == 'REQ':
                            answer = self.query_from_MES + work_with_DB.get_last_receiving_data(
                                self.port)
                            log.debug('{0} | sent to MES     | {1}'.format(self.port,
                                                                         answer))
                            self.conn.send(bytearray(answer, 'utf-8'))
                        else:
                            answer = work_with_DB.upload_data(
                                self.query_from_MES[0:4000], self.port)
                            return_msg = self.query_from_MES[0:45] + answer
                            log.debug('{0} | sent to MES     | {1}'.format(self.port,
                                                                         return_msg))
                            self.conn.send(bytearray(return_msg, 'utf-8'))

                            if answer[0:2] == conf.SEND_ERROR:
                                log.warning(
                                    '{0} | connection closed'.format(self.port))
                                self.conn.close()
                                break
                    else:
                        log.debug('{0} | port listening'.format(self.port))
                        break
                except socket.error as e:
                    if e.errno == 10054:
                        log.exception(
                            '{0} | {1}'.format(self.port, type(e).__name__))
                        break
                except KeyboardInterrupt:
                    log.exception('Process Interrupted')
