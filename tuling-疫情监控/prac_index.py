from flask import Flask,request,render_template
import os,json

app1=Flask(__name__)
@app1.route('/index',methods=['POST','GET'])
def index():
    return render_template('prac_index.html', name={"wname": "猪三岁2", "yname": "小花猪"}, name1=["猪三岁", "猪脑壳", "臭猪"])

if __name__=='__main__':
    app1.run(debug=True, host='127.0.0.1', port=5100)

