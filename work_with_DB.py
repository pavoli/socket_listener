# -*- coding: utf-8 -*-
__author__ = 'p.olifer'

import cx_Oracle

# GCS_DB_PARAMETER = '*****'
GCS_DB_PARAMETER = '*****'


def create_connection():
    con = cx_Oracle.connect(GCS_DB_PARAMETER)
    return con


def upload_data(new_data, port):
    """
    функция вставки данных в БД
    """
    con = create_connection()
    cursor = con.cursor()
    params = [new_data, port]
    answer = cursor.callfunc('pkg_jis_shortage_monitor.fnc_insert_data', cx_Oracle.STRING, params)

    con.commit()
    cursor.close()
    con.close()

    return answer


def get_last_receiving_data(port):
    """
    функция, которая находит и отправляет
    последние полученные данные от MES
    """
    con = create_connection()
    cursor = con.cursor()
    params = [port]
    answer = cursor.callfunc('pkg_jis_shortage_monitor.get_last_receiving_data', cx_Oracle.STRING, params)

    con.commit()
    cursor.close()
    con.close()

    return answer
