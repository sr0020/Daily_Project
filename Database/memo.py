# 0416

import pymysql
from flask import Flask, render_template, request

db = pymysql.connect(host="localhost",
                     port=3306,
                     user='root',
                     passwd='sarah164!!', # 빼 놓기
                     db='mysql',
                     charset='utf8')

cursor = db.cursor()

sql = "select * from 제품"

cursor.execute(sql)

data_list = cursor.fetchall()

app = Flask(__name__)
@app.route('/')
def index():
    sql = "select * from 제품"
    cursor.execute(sql)
    data_list = cursor.fetchall()

    return render_template('index.html', data_list=data_list)

if __name__=="__main__":
    app.run(debug=True)