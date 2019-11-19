# -*- coding:utf-8 -*-

from flask import Flask,request,jsonify,send_from_directory,make_response
import json
import os
import pymysql

app = Flask(__name__)
IMAGE_FOLDER = 'ChineseBQB'
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['JSON_AS_ASCII'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])

conn = pymysql.connect(host='111.230.153.254',port=3306,user='stickers', passwd='stickers', db='stickers',charset='utf8')
cursor =conn.cursor()

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello Tsdfhere!</h1>"

'''
/**
* showdoc
* @catalog 接口/获取表情包分类
* @title 获取表情包分类
* @description 获取表情包分类的接口
* @method get
* @url http://111.230.153.254/api/category
* @return {"code":0,"data":[{"cid":1,"category":"杰尼龟"},{"cid":"1","category":"杰尼龟"}]}
* @return_param code int 状态
* @return_param cid int 分类id
* @return_param category string 分类名称
* @number 99 
*/
'''

@app.route('/api/category', methods=['GET', 'POST'])
def get_categories():
    if request.method == 'GET':
        try:
            with conn.cursor() as cursor:
                sql = 'SELECT cid,category FROM categories'
                cursor.execute(sql)
                resultall = cursor.fetchall()
                print(resultall)
            conn.commit()
        finally:
            cursor.close()
        list = []
        for item in resultall:
            dict = {}
            dict['category'] = item[1]
            dict['cid'] = item[0]
            list.append(dict)
        return jsonify({'code' : 0, 'data': list})
    else:
        return '这是一个get请求'

@app.route('/api/category/<int:cid>', methods=['GET'])
def get_category(cid):
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT cid,category FROM categories'
            cursor.execute(sql)
            resultall = cursor.fetchall()
            print(resultall)
        conn.commit()
    finally:
        cursor.close()
    return jsonify({'task': resultall})

@app.route('/collection', methods=['GET', 'POST'])
def get_collection():
    if request.method == 'POST':
        pass

@app.route('/make', methods=['GET', 'POST'])
def get_make():
    if request.method == 'POST':
        print(type(request.get_data()))
        print(json.loads(request.get_data()))
        return '这是一个post请求 m'
    else:
        print(request.json())
        return '这是一个get请求 m'



@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('test', filename)):
            return send_from_directory('test', filename, as_attachment=True)
        pass


# show photo
@app.route('/large/<string:folder>/<string:filename>', methods=['GET'])
def show_photo(folder, filename):
    file_dir = os.path.join(basedir, app.config['IMAGE_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % folder, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass



if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)