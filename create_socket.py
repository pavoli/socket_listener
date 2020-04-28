# -*- coding: utf-8 -*-
#! /usr/local/bin/python3
__author__ = 'p.olifer'


import socket
import logging
from goto import with_goto

import work_with_DB
import conf


logging.basicConfig(
    filename=conf.LOG_FILE_NAME,
    level=logging.DEBUG,
    format='%(asctime)s | %(message)s'
)


class socket_server():
    def __init__(self, ip, port):

        # self.ip = socket.gethostbyname(socket.gethostname())
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info('{} | create socket'.format(self.port))

        self.sock.bind((self.ip, self.port))
        logging.info('{} | bind to socket'.format(self.port))

        self.sock.listen(5)
        logging.info('{} | listen socket'.format(self.port))


    @with_goto
    def create(self):
        label .begin
        self.conn, self.addr = self.sock.accept()
        logging.info('{} | accept connection'.format(self.port))

        self.conn.setblocking(1)

        while True:
            try:
                self.query_from_MES = self.conn.recv(10000).strip().decode('utf-8')

                if not len(self.query_from_MES) == 0:
                    logging.info('{} | receive data    | {}'.format(self.port, self.query_from_MES))
                    flag = self.query_from_MES[0:3]
                    logging.info('{} | flag            | {}'.format(self.port, flag))

                    if flag == 'REQ':
                        answer = self.query_from_MES + work_with_DB.get_last_receiving_data(self.port)
                        logging.info('{} | sent to MES     | {}'.format(self.port, answer))

                        self.conn.send(bytearray(answer, 'utf-8'))
                    else:
                        answer = work_with_DB.upload_data(self.query_from_MES[0:4000], self.port)
                        return_msg = self.query_from_MES[0:45] + answer
                        logging.info('{} | sent to MES     | {}'.format(self.port, return_msg))

                        self.conn.send(bytearray(return_msg, 'utf-8'))

                        if answer[0:2] == conf.SEND_ERROR:
                            logging.WARNING('{} | connection closed'.format(self.port))
                            self.conn.close()
                            try:
                                logging.warning('{} | restart server'.format(self.port))
                                s1 = socket_server(self.ip, self.port)
                                s1.run()
                            except Exception as e:
                                # returns the name of the exception
                                logging.exception('{} | {} | {}'.format(self.port, type(e).__name__, e.message))
                else:
                    goto.begin
                    logging.info('{} | goto .begin'.format(self.port))
            except socket.error as e:
                if e.errno == 10054:
                    goto.begin
                    logging.exception('{} | {} | {}'.format(self.port, type(e).__name__, e.message))