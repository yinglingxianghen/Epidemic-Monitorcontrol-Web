# encoding: utf-8



import pymysql

def get_conn():
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='111111',db='yiqingjiankong',charset='utf8')
    course =conn.cursor()
    return conn,course



print(get_conn())
