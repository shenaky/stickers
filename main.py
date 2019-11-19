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

db = pymysql.connect(host='111.230.153.254',port=3306,user='stickers', passwd='stickers', db='stickers',charset='utf8')
cursor = db.cursor()

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello Tsdfhere!</h1>"

@app.route('/category', methods=['GET', 'POST'])
def get_categories():
    if request.method == 'GET':
        try:
            with conn.cursor() as cursor:
                sql = 'SELECT cid,category FROM categories'
                cursor.execute(sql)
                # result = cursor.fetchone()
                resultall = cursor.fetchall()
                # fetchmany
                # print(result)
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
        return jsonify({'code' : 0, 'categories': list})
    else:
        return '这是一个get请求'

@app.route('/category/<int:cid>', methods=['GET'])
def get_category(cid):
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT cid,category FROM categories'
            cursor.execute(sql)
            # result = cursor.fetchone()
            resultall = cursor.fetchall()
            # fetchmany
            # print(result)
            print(resultall)
        conn.commit()
    finally:
        cursor.close()
    #有的话，就返回列表形式包裹的这个元素，没有的话就报错404   
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})
    #否则，将这个task以json的格式返回。

@app.route('/collection', methods=['GET', 'POST'])
def get_collection():
    if request.method == 'POST':
        pass

@app.route('/make', methods=['GET', 'POST'])
def get_make():
    if request.method == 'POST':
        print(type(request.get_data()))
        print(json.loads(request.get_data()))
        return jsonify({'tasks': tasks})
        return '这是一个post请求 m'
    else:
        print(request.json())
        return jsonify({'tasks': tasks})
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