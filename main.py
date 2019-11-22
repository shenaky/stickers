# -*- coding:utf-8 -*-

from flask import Flask,request,jsonify,send_from_directory,make_response
from random import shuffle
import json
import os
import requests
import pymysql
from auth_token import create_token,verify_token,login_required

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
* @catalog 用户相关
* @title 用户登录
* @description 用户登录的接口
* @method post
* @url  http://111.230.153.254/api/login
* @param js_code 必选 string 登录时获取的 code
* @return {"code":0,"msg":"success","token":"tokentoken"}
* @return_param code int 状态
* @return_param msg string 消息
* @return_param token string token
* @number 1
*/
'''
@app.route("/api/login",methods=["POST"])
def login():
    '''
    用户登录
    :return:token
    '''
    try:
        js_code = request.args.get('js_code')
    except:
        return jsonify(code = 4103,msg = "未接收到参数")

    
    #校验参数
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    querystring = {
            "appid": "wxd257872efc01ad6c",
            "secret": "8b48a7c1e2c68c6f7c78546a22e2c48f",
            "js_code": js_code,
            "grant_type": "authorization_code"
        }
    r = requests.get(url, params=querystring)
    errcode = r.json()['errcode']
    try:
        openid = r.json()['openid']
    except:
        return jsonify(code = 4103,msg = "openid获取失败")
    
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT uid FROM users WHERE openid = %s'
            cursor.execute(sql, (openid))
            result = cursor.fetchone()
        conn.commit()
    finally:
        cursor.close()
    if not result:
        try:
            cursor.execute("INSERT INTO users (openid) VALUES (%s)", (openid))
            cursor.connection.commit()
        except:
            print("sql insert error")
            conn.rollback()
        finally:
            cursor.close()
    
    #创建token
    token = create_token(openid)
    print(token)

    #把token返回给前端
    # return jsonify(code=0,msg="succeed",data=token)
    return jsonify({'code' : 0, 'msg': 'success', 'token': list})

'''
/**
* showdoc
* @catalog 接口
* @title 获取表情包主页
* @description 获取表情包主页的接口
* @method get
* @url http://111.230.153.254/api/home
* @return {"code":0, "data":[{"sid":1,"url":"http://111.230.153.254/large/052Squirtle_%E6%9D%B0%E5%B0%BC%E9%BE%9F/Squirtle22.JPG"},{"cid":"1","url":"http://111.230.153.254/large/052Squirtle_%E6%9D%B0%E5%B0%BC%E9%BE%9F/Squirtle22.JPG"}]}
* @return_param code int 状态
* @return_param sid int 表情id
* @return_param url string url
*/
'''

@app.route('/api/home', methods=['GET'])
def get_home():
    limit = 18
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT sid,url FROM stickers ORDER BY RAND() LIMIT %s'
            cursor.execute(sql, (limit))
            resultall = cursor.fetchall()
            # print(resultall)
        conn.commit()
    finally:
        cursor.close()
    list = []
    for item in resultall:
        dict = {}
        dict['sid'] = item[0]
        dict['url'] = item[1]
        list.append(dict)
    # shuffle(list) 
    return jsonify({'code' : 0, 'data': list})

'''
/**
* showdoc
* @catalog 接口
* @title 获取表情包分类
* @description 获取表情包分类的接口
* @method get
* @url http://111.230.153.254/api/category
* @return {"code":0,"data":[{"cid":1,"category":"杰尼龟","sid":1,"url":"http://111.230.153.254/large/001Funny/Funny00020.gif"},{"cid":1,"category":"杰尼龟","sid":1,"url":"http://111.230.153.254/large/001Funny/Funny00020.gif"}]}
* @return_param code int 状态
* @return_param cid int 分类id
* @return_param category string 分类名称
* @return_param sid int 表情id
* @return_param url string 表情url
*/
'''

@app.route('/api/category', methods=['GET', 'POST'])
def get_categories():
    if request.method == 'GET':
        try:
            with conn.cursor() as cursor:
                sql = '''SELECT categories.cid,categories.category,any_value(stickers.sid),any_value(url)
                        FROM stickers,belong,categories
                        WHERE stickers.sid = belong.sid AND belong.cid = categories.cid
                        GROUP BY cid,category'''
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
            dict['sid'] = item[2]
            dict['url'] = item[3]
            list.append(dict)
        return jsonify({'code' : 0, 'data': list})
    else:
        return '这是一个get请求'

'''
/**
* showdoc
* @catalog 接口
* @title 获取一类表情包的url
* @description 获取一类表情包的url的接口
* @method get
* @url http://111.230.153.254/api/category/<int:cid>
* @param limit 必选 int 每页条数
* @param page 必选 int 页数
* @return {"code":0,"cid" : 12, "data":[{"sid":1,"url":"http://111.230.153.254/large/052Squirtle_%E6%9D%B0%E5%B0%BC%E9%BE%9F/Squirtle22.JPG"},{"sid":"1","url":"http://111.230.153.254/large/052Squirtle_%E6%9D%B0%E5%B0%BC%E9%BE%9F/Squirtle22.JPG"}]}
* @return_param code int 状态
* @return_param cid int 分类id
* @return_param sid int 表情id
* @return_param url string url
*/
'''

@app.route('/api/category/<int:cid>', methods=['GET'])
def get_category(cid):
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    offset = limit * page
    try:
        with conn.cursor() as cursor:
            sql = 'SELECT sid,url FROM stickers WHERE sid IN (SELECT sid FROM belong WHERE cid = %s) ORDER BY sid DESC LIMIT %s OFFSET %s'
            cursor.execute(sql, (cid, limit, offset))
            resultall = cursor.fetchall()
        conn.commit()
    finally:
        cursor.close()
    list = []
    for item in resultall:
        dict = {}
        dict['sid'] = item[0]
        dict['url'] = item[1]
        list.append(dict)
    return jsonify({'code' : 0, 'cid' : cid, 'data': list})
    
    # return jsonify({'task': resultall})

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

# @app.route('/images/<string:folder>/<string:filename>', methods=['GET'])
# def get_download(filename):
#     file_dir = os.path.join(basedir, app.config['IMAGE_FOLDER'])
#     if request.method == "GET":
#         if os.path.isfile(os.path.join('test', filename)):
#             return send_from_directory('test', filename, as_attachment=True)
#         pass


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