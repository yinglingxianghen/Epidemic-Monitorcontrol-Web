# encoding: utf-8
"""
@author: 夏洛
@QQ: 1972386194
@file: crawl.py
"""
import re
import sys
import traceback


'''
30 * * * * python /usr/local/scripts/crawl.py up_his >> /usr/local/scripts/log_his 2>&1 &
*/5 * * * * python /usr/local/scripts/crawl.py up_det >> /usr/local/scripts/log_det 2>&1 &
'''

import requests,time,pymysql
import json
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=jQuery34102848205531413024_1584924641755&_=1584924641756'
headers ={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
}
res = requests.get(url,headers=headers)

def crawl():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    res = requests.get(url)
    d = json.loads(res.text)
    data_all = json.loads(d['data'])
    lt = data_all['lastUpdateTime']  # 数据时间
    ct = data_all['chinaTotal']  # 当前汇总数据
    ca = data_all['chinaAdd']   #
    # print(data_all)
    details = []  # 单天数据
    update_time = data_all['lastUpdateTime']
    data_country = data_all['areaTree']
    for pro_infos in data_country[0]['children']:
        province = pro_infos['name']  # 省名
        for city_infos in pro_infos['children']:
            city = city_infos['name']  # 市名
            confirm = city_infos['total']['confirm']  # 历史总数
            confirm_add = city_infos['today']['confirm']  # 今日增加数
            heal = city_infos['total']['heal']  # 治愈
            dead = city_infos['total']['dead']  # 死亡
            details.append([update_time,province, city, confirm, confirm_add, heal, dead])
    return details

# crawl()


def crawl2():
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare'
    res = requests.get(url)
    data = res.json()
    params = data.get('data')
    chinaDayList = params['chinaDayList']  # 历史记录
    chinaDayAddList = params['chinaDayAddList']  # 历史新增记录
    history = {}  # 历史数据
    for i in chinaDayList:
        ds = '2021.' + i['date']  # 时间
        tup = time.strptime(ds, '%Y.%m.%d')
        ds = time.strftime('%Y-%m-%d', tup)  # 改变时间格式，插入数据库
        confirm = i['confirm']
        suspect = i['suspect']
        heal = i['heal']
        dead = i['dead']
        history[ds] = {'confirm': confirm, 'suspect': suspect, 'heal': heal, 'dead': dead}
    for i in chinaDayAddList:
        ds = '2021.' + i['date']  # 时间
        tup = time.strptime(ds, '%Y.%m.%d')
        ds = time.strftime('%Y-%m-%d', tup)  # 改变时间格式，插入数据库
        confirm_add = i['confirm']
        suspect_add = i['suspect']
        heal_add = i['heal']
        dead_add = i['dead']
        history[ds].update(
            {'confirm_add': confirm_add, 'suspect_add': suspect_add, 'heal_add': heal_add, 'dead_add': dead_add})

    for k, v in history.items():
        print(k,"|",v)
# crawl2()
    return history



def crawl3():
    headers = {
        "cookie": "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFfil5957iJyCJO57B-3ufP5NHD95QNSoz4eKBcSoncWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0qE1K2XSoqRSntt; SUB=_2AkMXiL0OdcPxrARXmvEUyG3kZItH-jykXdT4An7oJhMyPRh77kQkqSdutBF-XCBCZd-Lcmy0fSH-r6x0fJ8OUhUP; _T_WM=81631151762; WEIBOCN_FROM=1110006030; MLOGIN=0; XSRF-TOKEN=742063",
        "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Mobile Safari/537.36"
    }
    start_url = 'https://m.weibo.cn/comments/hotflow?id=4669021482388139&mid=4669021482388139&max_id_type=0'
    response = requests.get(start_url, headers=headers)
    if response.status_code == 200:
        response = response.json()
        # max_id = response['data']['max_id']
        content_list = response.get("data").get('data')
        texts = []
        for item in content_list:
            # create_time = item['created_at']
            text = "".join(re.findall('[\u4e00-\u9fa5]', item["text"]))
            # user_id = item.get("user")["id"]
            user_name = item.get("user")["screen_name"]
            # print([count, create_time, user_id, user_name, text])
            #     csv_data([count, create_time, user_id, user_name, text])
            texts.append([text,user_name])
        return texts

def get_conn():
    # :return:连接，游标
    # 建立连接
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="111111",
                           db="yiqingjiankong",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    return conn,cursor

def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def update_details():
    # 更新detail表:return:
    cursor = None
    conn = None
    try:
        li = crawl()   # 0是历史数据字典，1是最新详细数据列表
        conn,cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)'  # 对比当前最大时间戳
        # 根据时间对比 数据是否更新 时间不想等就是数据被更新
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)

def insert_history():
    # 插入历史数据
    cursor = None
    conn = None
    try:
        dic = crawl2() #
        print(f"{time.asctime()}开始插入历史数据")
        conn,cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k, v in dic.items():
            cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                 v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                 v.get("dead"), v.get("dead_add")])
        conn.commit()   # 提交事务
        print(f"{time.asctime()}插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_history():
    # 更新历史数据
    cursor = None
    conn = None
    try:
        dic = crawl2() # 0是历史数据字典，1是最新详细数据列表
        print(f"{time.asctime()}开始更新历史数据")
        conn,cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        # select confirm history where ds = "2021-07-23 00:00:00"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            if not cursor.execute(sql_query,k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])
        conn.commit()   # 提交事务
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def insert_texts():
    cursor = None
    conn = None
    try:
        dic = crawl3() # 0是历史数据字典，1是最新详细数据列表
        print(f"{time.asctime()}开始更新历史数据")
        conn,cursor = get_conn()
        # [[a,b,c],[d,f,g],[q,w,e]]
        sql = "insert into text(update_time,content,username) values ('2021-08-12 14:08:37',%s,%s)"
        for item in dic:
            print(item)
            cursor.execute(sql, item)
        conn.commit()   # 提交事务
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

if __name__ == '__main__':
    # l = len(sys.argv)
    # if l == 1:
    #     s = '''
    #         up_his  更新历史数据
    #         up_det  更新详细数据
    #     '''
    #     print(s)
    # else:
    #     order = sys.argv[1]
    #     if order == 'up_his':
    #         update_history()
    #     elif order == 'up_det':
    #         update_details()

    # insert_history()
    update_history()
