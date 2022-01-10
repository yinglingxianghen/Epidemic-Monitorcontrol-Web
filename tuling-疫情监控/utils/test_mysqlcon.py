#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql

# 查询所有字段
def list_col(host, user, port,password, database, tabls_name):
    db = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='111111',db='yiqingjiankong',charset='utf8')
    cursor = db.cursor()
    cursor.execute("select * from %s" % tabls_name)
    col_name_list = [tuple[0] for tuple in cursor.description]
    db.close()
    return col_name_list

# 列出所有的表
def list_table(host,port,user,password,db):
    # db = pymysql.connect(host,user,port,password,db)
    db = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='111111',db='yiqingjiankong',charset='utf8')
    cursor = db.cursor()
    cursor.execute("show tables")
    table_list = [tuple[0] for tuple in cursor.fetchall()]
    db.close()
    return table_list

user = "root" # 用户名
password = "111111" # 连接密码
host = "127.0.0.1" # 连接地址
db = "yiqingjiankong" # 数据库名
port=3306
tables = list_table(host, port,user, password, db) # 获取所有表，返回的是一个可迭代对象
print(tables) 

for table in tables:
    col_names = list_col(host, port,user, password, db, table)
    print(col_names) # 输出所有字段名
