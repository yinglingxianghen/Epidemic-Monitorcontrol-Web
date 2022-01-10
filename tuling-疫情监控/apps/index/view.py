# !/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
project:class1
author:lanyu 2020/5/2
"""
import collections

import jieba
from flask import request
from . import a1
from flask import render_template,jsonify

@a1.route('/')
def index():
    return render_template('main.html')


from utils import times
@a1.route('/time')
def get_time():
    return times.get_time()

# 渲染总数量
@a1.route('/c1')
def get_c1_data():
    data = times.get_c1_data()
    return jsonify({"confirm":data[0],"suspect":data[1],"heal":data[2],"dead":data[3]})

# 地图数据
@a1.route('/c2')
def get_c2_data():
    res = []
    for i in times.get_c2_data():
        res.append({'name':i[0],"value":int(i[1])})
    # res = [{"name":'北京',"value":1000},{"name":'上海',"value":2342},{"name":'湖北',"value":12342}]
    return jsonify({'data':res})

# 折线图数据
@a1.route('/l1')
def get_l1_data():
    data = times.get_l1_data()
    day,confirm,suspect,heal,dead = [],[],[],[],[]
    for a,b,c,d,e in data[7:]:  # 砍掉前7天数据
        day.append(a.strftime('%m-%d'))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day":day,"confirm":confirm,"suspect":suspect,"heal":heal,"dead":dead})

# 折线图数据

@a1.route('/l2')
def get_l2_data():
    """
    :return:
    """
    data = times.get_l2_data()
    day,confirm_add,suspect_add =[],[],[]
    for a,b,c in data[7:]:  # 砍掉前7天数据
        day.append(a.strftime('%m-%d'))
        confirm_add.append(b)
        suspect_add.append(c)
    print(day)

    return jsonify({"day":day,"confirm_add":confirm_add,"suspect_add":suspect_add})


# 柱状图数据
@a1.route('/r1')
def get_r1_data():
    data = times.get_r1_data()
    title,num  = [],[]
    for i in data:
        title.append(i[0])
        num.append(int(i[1]))
    return jsonify({'title': title,'num':num})

import string
from jieba.analyse import extract_tags
# 热门搜索数据展示
@a1.route('/r2')
def get_r2_data():
    ff = []
    data = times.get_text_data()
    # [('sdadas'),('asdasdsa')]
    text = []
    for i in data:
        text.append(i[0])
    new_data = '/'.join(text)
    # print(new_data)
    seg_list_exact = jieba.cut(new_data, cut_all=False)
    with open(r'D:\PycharmProjects\tuling-疫情监控代码(1)\tuling-疫情监控\apps\index\baidu_stopwords.txt', encoding='utf-8') as f:
        con = f.read().split('\n')
        # 转集合去重
        stop_words = set()
        for i in con:
            print(i)
            stop_words.add(i)
    # 迭代分词库
    result_list = []
    for word in seg_list_exact:
        # 设置停用词并去除单个词
        if word not in stop_words and len(word) > 1:
            # 追加到列表
            result_list.append(word)
    # 筛选后统计词频
    word_counts = collections.Counter(result_list)
    # print(word_counts)
    for i, v in word_counts.items():
        ff.append({'name':i,'value':v})
    # [{'name': '你好呀','value':'123456'},{'name': '你好呀','value':'123456'},{'name': '你好呀','value':'123456'}]
    return jsonify({'kws':ff})


@a1.route('/ditu')
def ditu():
    return render_template('ditu.html')
