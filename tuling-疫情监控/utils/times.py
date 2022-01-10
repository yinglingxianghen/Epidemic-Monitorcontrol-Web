# !/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
project:class1
author:lanyu 2020/5/2
"""

# https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1
# https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1



import time

# 获取服务器的时间
def  get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format('年','月','日')

import pymysql

def get_conn():
    conn = pymysql.connect(host='101.200.62.28',port=3306,user='root',password='xiaozhang',db='feifei',charset='utf8')
    course =conn.cursor()
    return conn,course


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql,*args):
    # 封装通用查询，返回查询结果
    conn,cursor = get_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_conn(conn,cursor)
    return res

def get_c1_data():
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal)," \
          "sum(dead) " \
          "from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)
    return res[0]



def get_c2_data():
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res


def get_l1_data():
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res

def get_l2_data():
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res

# SELECT city,confirm GROUP_CONCAT(confirm) FROM detalis  GROUP BY province ;

'''
select * from details where province = '湖南' and update_time=(select update_time from details " \
          "order by update_time desc limit 1)

'''

def get_r1_data():
    sql = "select city,confirm from (select * from details where province = '湖南' and update_time=(select update_time from details order by update_time desc limit 1)) as ss ORDER BY confirm DESC LIMIT 5"
    # sql1 = 'select city,confirm from (select city,confirm from details where '
    res = query(sql)
    return res

# def get_r2_data():
#     """
#     :return:  返回20条热门数据
#     """
#     sql = 'select content from hostsearch order_by desc limit 20'
#     res = query(sql)
#     return res


def get_text_data():
    '''
    返回 热搜数据
    :return:
    '''
    sql = 'select content from text'
    res = query(sql)
    return res


