# -*- coding:utf-8 -*-
import datetime
import random

from flask import Flask, request, jsonify, send_from_directory, make_response
import os
import requests
from werkzeug.utils import secure_filename
from auth_token import create_token, verify_token, login_required
from db_execute import execute_all, execute_eff

app = Flask(__name__)
IMAGE_FOLDER = 'ChineseBQB'
SECRET_KEY = 'stickersormeme'
UPLOAD_FOLDER = 'ChineseBQB/make'
app.config["SECRET_KEY"] = SECRET_KEY
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'}


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There cur util pool one all!</h1>"


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


@app.route("/api/login", methods=["POST"])
def login():
    """
    用户登录
    :return:token
    """
    res_dir = request.get_json()
    if res_dir is None:
        # 这里的code，依然推荐用一个文件管理状态
        return jsonify(code=4103, msg="未接收到参数")

    # 获取前端传过来的参数
    js_code = res_dir.get("js_code")
    print(js_code)

    # 校验参数
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    querystring = {
        "appid": "wxd257872efc01ad6c",
        "secret": "8b48a7c1e2c68c6f7c78546a22e2c48f",
        "js_code": js_code,
        "grant_type": "authorization_code"
    }
    r = requests.get(url, params=querystring)
    # try:
    #     openid = r.json()['openid']
    # except:
    #     print(r.json())
    #     return jsonify(code=4103, msg="openid获取失败")
    if 'openid' in r.json():
        openid = r.json()['openid']
    else:
        print(r.json())
        return jsonify(code=4103, msg="openid获取失败")
    print(openid)

    # 检测是否注册
    sql = 'SELECT uid FROM users WHERE openid = %s'
    result = execute_all(sql, (openid,))
    if not result:
        sql = 'INSERT INTO users (openid) VALUES (%s)'
        execute_eff(sql, openid)
        sql = 'SELECT uid FROM users WHERE openid = %s'
        result = execute_all(sql, (openid,))
        item = result[0]
        uid = item[0]
    else:
        item = result[0]
        uid = item[0]
    # 创建token
    token = create_token(uid)
    print(token)

    return jsonify({'code': 0, 'msg': 'success', 'token': token})


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
    sql = 'SELECT sid,url FROM stickers ORDER BY RAND() LIMIT %s'
    resultall = execute_all(sql, limit)
    lis = []
    for item in resultall:
        dic = {}
        dic['sid'] = item[0]
        dic['url'] = item[1]
        lis.append(dic)
    return jsonify({'code': 0, 'data': lis})


'''
/**
* showdoc
* @catalog 接口
* @title 获取表情包分类
* @description 获取表情包分类的接口
* @method get
* @url http://111.230.153.254/api/category
* @param limit 必选 int 每页条数
* @param page 必选 int 页数
* @return {"code":0,"data":[{"cid":1,"category":"杰尼龟","sid":1,"url":"http://111.230.153.254/large/001Funny/Funny00020.gif"},{"cid":1,"category":"杰尼龟","sid":1,"url":"http://111.230.153.254/large/001Funny/Funny00020.gif"}]}
* @return_param code int 状态
* @return_param cid int 分类id
* @return_param category string 分类名称
* @return_param sid int 表情id
* @return_param url string 表情url
*/
'''


@app.route('/api/category', methods=['GET'])
def get_categories():
    if request.method == 'GET':
        limit = int(request.args.get('limit'))
        page = int(request.args.get('page'))
        offset = limit * page
        sql = '''SELECT categories.cid,categories.category,any_value(stickers.sid),any_value(url)
                 FROM stickers,belong,categories
                 WHERE stickers.sid = belong.sid AND belong.cid = categories.cid
                 GROUP BY cid,category
                 ORDER BY cid DESC LIMIT %s OFFSET %s'''
        resultall = execute_all(sql, (limit, offset))
        lis = []
        for item in resultall:
            dic = {}
            dic['category'] = item[1]
            dic['cid'] = item[0]
            dic['sid'] = item[2]
            dic['url'] = item[3]
            lis.append(dic)
        return jsonify({'code': 0, 'data': lis})
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
    sql = 'SELECT sid,url FROM stickers WHERE sid IN (SELECT sid FROM belong WHERE cid = %s) ORDER BY sid DESC LIMIT %s OFFSET %s'
    resultall = execute_all(sql, (cid, limit, offset))
    lis = []
    for item in resultall:
        dic = {}
        dic['sid'] = item[0]
        dic['url'] = item[1]
        lis.append(dic)
    return jsonify({'code': 0, 'cid': cid, 'data': lis})


'''
/**
* showdoc
* @catalog 收藏接口
* @title 获取所有收藏夹
* @description 获取所有收藏夹的接口
* @method get
* @url http://111.230.153.254/api/collection
* @header token 必选 sting token
* @return {"code":0, "data":[{"collect_id":1,"collect_name":"收藏夹"},{"collect_id":1,"collect_name":"收藏夹"}]}
* @return_param code int 状态
* @return_param collect_id int 收藏夹id
* @return_param collect_name string 收藏夹名称
* @number 20
*/
/**
* showdoc
* @catalog 收藏接口
* @title 新建收藏夹
* @description 新建收藏夹的接口
* @method post
* @url http://111.230.153.254/api/collection
* @header token 必选 sting 认证token
* @param collect_name 必选 string 收藏夹名称
* @return {"code" : 0, "msg": "succeed"}
* @return_param code int 状态
* @return_param msg string 信息
* @number 21
*/
/**
* showdoc
* @catalog 收藏接口
* @title 删除收藏夹
* @description 删除收藏夹的接口
* @method delete
* @url http://111.230.153.254/api/collection
* @header token 必选 sting 认证token
* @param collect_id 必选 int 收藏夹id
* @return {"code" : 0, "msg": "succeed"}
* @return_param code int 状态
* @return_param msg string 信息
* @number 22
*/
'''


@app.route('/api/collection', methods=['GET', 'DELETE', 'POST'])
@login_required
def get_allfiles():
    token = request.headers["token"]
    uid = verify_token(token)
    print(uid)
    if not uid:
        return jsonify(code=4100, msg="token失效")

    if request.method == 'GET':
        sql = 'SELECT collect_id,collect_name FROM collection WHERE uid = %s'
        resultall = execute_all(sql, uid)
        lis = []
        for item in resultall:
            dic = {}
            dic['collect_id'] = item[0]
            dic['collect_name'] = item[1]
            lis.append(dic)
        return jsonify({'code': 0, 'data': lis})

    elif request.method == 'DELETE':
        res_dir = request.get_json()
        if res_dir is None:
            return jsonify(code=4103, msg="未接收到参数")
        collect_id = res_dir.get("collect_id")
        sql = 'delete from collection where collect_id = %s'
        execute_eff(sql, collect_id)
        sql = 'delete from collect where collect_id = %s'
        effect_row = execute_eff(sql, collect_id)
        print(effect_row)
        return jsonify({'code': 0, 'msg': 'succeed'})

    elif request.method == 'POST':
        res_dir = request.get_json()
        if res_dir is None:
            return jsonify(code=4103, msg="未接收到参数")
        collect_name = res_dir.get("collect_name")
        sql = "INSERT INTO collection (uid, collect_name) VALUES (%s, %s)"
        effect_row = execute_eff(sql, (uid, collect_name))
        print(effect_row)
        return jsonify({'code': 0, 'msg': 'succeed'})


'''
/**
* showdoc
* @catalog 收藏接口
* @title 获取收藏夹中的表情
* @description 获取收藏夹中的表情的接口
* @method get
* @url http://111.230.153.254/api/collection/<int:collect_id>
* @header token 必选 sting token
* @return {"code":0, "data":[{"coid":1,"sid": 1, "url": "url"},{"coid":1,"sid": 1, "url": "url"}]}
* @return_param code int 状态
* @return_param coid int 收藏id
* @return_param sid int 表情id
* @return_param url string 表情url
* @number 23
*/
/**
* showdoc
* @catalog 收藏接口
* @title 新建收藏
* @description 新建收藏的接口
* @method post
* @url http://111.230.153.254/api/collection/<int:collect_id>
* @header token 必选 sting 认证token
* @param sid 必选 int 表情id
* @param cid 可选 int 分类id
* @return {"code" : 0, "msg": "succeed"}
* @return_param code int 状态
* @return_param msg string 信息
* @number 24
*/
/**
* showdoc
* @catalog 收藏接口
* @title 删除收藏
* @description 删除收藏的接口
* @method delete
* @url http://111.230.153.254/api/collection/<int:collect_id>
* @header token 必选 sting 认证token
* @param coid 必选 int 收藏id
* @return {"code" : 0, "msg": "succeed"}
* @return_param code int 状态
* @return_param msg string 信息
* @number 25
*/
'''


@app.route('/api/collection/<int:collect_id>', methods=['GET', 'DELETE', 'POST'])
@login_required
def get_file(collect_id):
    if request.method == 'GET':
        sql = 'SELECT coid,stickers.sid,url FROM collect,stickers WHERE stickers.sid = collect.sid AND collect_id = %s'
        resultall = execute_all(sql, collect_id)
        lis = []
        for item in resultall:
            dic = {}
            dic['coid'] = item[0]
            dic['sid'] = item[1]
            dic['url'] = item[2]
            lis.append(dic)
        return jsonify({'code': 0, 'data': lis})

    elif request.method == 'POST':
        res_dir = request.get_json()
        if res_dir is None:
            return jsonify(code=4103, msg="未接收到参数")
        if 'cid' in res_dir:
            cid = res_dir.get("cid")
            sql = '''INSERT INTO collect (collect_id, sid) 
                     SELECT %s ,sid 
                     FROM belong 
                     WHERE cid = %s '''
            effect_row = execute_eff(sql, (collect_id, cid))
        else:
            sid = res_dir.get("sid")
            sql = "INSERT INTO collect (collect_id, sid) VALUES (%s, %s)"
            effect_row = execute_eff(sql, (collect_id, sid))
        print(effect_row)
        return jsonify({'code': 0, 'msg': 'succeed'})

    elif request.method == 'DELETE':
        res_dir = request.get_json()
        if res_dir is None:
            return jsonify(code=4103, msg="未接收到参数")
        coid = res_dir.get("coid")
        sql = 'delete from collect where coid = %s'
        effect_row = execute_eff(sql, coid)
        print(effect_row)
        return jsonify({'code': 0, 'msg': 'succeed'})


'''
/**
* showdoc
* @catalog 接口
* @title 搜索表情包
* @description 搜索表情包的接口
* @method get
* @url http://111.230.153.254/api/search
* @param kw 必选 string 关键词
* @param limit 必选 int 每页条数
* @param page 必选 int 页数
* @return {"code":0, "data":[{"sid":1,"url":"http://111.230.153.254/large/052Squirtle/Squirtle30.JPG"},{"sid":1,"url":"http://111.230.153.254/large/052Squirtle/Squirtle30.JPG"}]}
* @return_param code int 状态
* @return_param sid int 表情id
* @return_param url string url
* @number 28
*/
'''


@app.route('/api/search', methods=['GET'])
def get_search():
    keyword = request.args.get("kw")
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    offset = limit * page
    sql = 'select sid,url from stickers where category like %s ORDER BY sid ASC LIMIT %s OFFSET %s'
    resultall = execute_all(sql, ("%" + keyword + "%", limit, offset))
    lis = []
    for item in resultall:
        dic = {}
        dic['sid'] = item[0]
        dic['url'] = item[1]
        lis.append(dic)
    return jsonify({'code': 0, 'data': lis})


'''
/**
* showdoc
* @catalog 制作接口
* @title 搜索表情包模板
* @description 搜索表情模板的接口
* @method get
* @url https://111.230.153.254/api/temps/search
* @param kw 必选 string 关键词
* @param limit 必选 int 每页条数
* @param page 必选 int 页数
* @return {"code":0, "data":[{"tid":1,"url":"http://111.230.153.254/large/temps/006tKfTcly1g1a7ucne35j30j60ewglu.jpg"},{"tid":1,"url":"http://111.230.153.254/large/temps/006tKfTcly1g1a7ucne35j30j60ewglu.jpg"}]}
* @return_param code int 状态
* @return_param tid int 模板id
* @return_param url string url
* @number 29
*/
'''


@app.route('/api/temps/search', methods=['GET'])
def get_temps_search():
    try:
        keyword = request.args.get("kw")
        limit = int(request.args.get('limit'))
        page = int(request.args.get('page'))
    except TypeError:
        return jsonify(code=4103, msg="缺少参数")
    offset = limit * page
    sql = 'select tid,url from templates where title like %s ORDER BY tid ASC LIMIT %s OFFSET %s'
    resultall = execute_all(sql, ("%" + keyword + "%", limit, offset))
    lis = []
    for item in resultall:
        dic = {}
        dic['tid'] = item[0]
        dic['url'] = item[1]
        lis.append(dic)
    return jsonify({'code': 0, 'data': lis})


'''
/**
* showdoc
* @catalog 制作接口
* @title 获取表情包模板
* @description 获取表情包模板的接口
* @method get
* @url http://111.230.153.254/api/temps
* @param limit 必选 int 每页条数
* @param page 必选 int 页数
* @return {"code":0, "data":[{"tid":1,"url":"http://111.230.153.254/large/temps/ceeb653ely1fkfupduos9j208c08cgm7.jpg"},{"tid":1,"url":"http://111.230.153.254/large/temps/ceeb653ely1fkfupduos9j208c08cgm7.jpg"}]}
* @return_param code int 状态
* @return_param tid int 模板id
* @return_param url string url
* @number 27
*/
'''


@app.route('/api/temps', methods=['GET'])
def get_temps():
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    offset = limit * page
    sql = 'SELECT tid,url FROM templates ORDER BY tid ASC LIMIT %s OFFSET %s'
    resultall = execute_all(sql, (limit, offset))
    lis = []
    for item in resultall:
        dic = {}
        dic['tid'] = item[0]
        dic['url'] = item[1]
        lis.append(dic)
    return jsonify({'code': 0, 'data': lis})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def create_uuid():
    # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum


@app.route('/api/make', methods=['GET', 'DELETE', 'POST'])
@login_required
def get_make():
    token = request.headers["token"]
    uid = verify_token(token)
    print(uid)
    if not uid:
        return jsonify(code=4100, msg="token失效")

    if request.method == 'GET':
        sql = 'SELECT mid,tid,url FROM make WHERE uid = %s'
        resultall = execute_all(sql, uid)
        lis = []
        for item in resultall:
            dic = {}
            dic['mid'] = item[0]
            dic['tid'] = item[1]
            dic['url'] = item[2]
            lis.append(dic)
        return jsonify({'code': 0, 'data': lis})

    elif request.method == 'POST':
        file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = request.files['image']
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            print(fname)
            ext = fname.rsplit('.', 1)[1]
            new_filename = create_uuid() + '.' + ext
            f.save(os.path.join(file_dir, new_filename))
            filename = new_filename
            url = 'http://111.230.153.254/large/' + 'make' + '/' + filename
            sql = "INSERT INTO make (uid, url, filename) VALUES (%s, %s, %s)"
            effect_row = execute_eff(sql, (uid, url, filename))
            return jsonify({"code": 0, "msg": "上传成功"})
        else:
            return jsonify({"code": 1001, "msg": "上传失败"})

    elif request.method == 'DELETE':
        res_dir = request.get_json()
        if res_dir is None:
            return jsonify(code=4103, msg="未接收到参数")
        mid = res_dir.get("mid")
        sql = 'delete from make where mid = %s AND uid = %s'
        effect_row = execute_eff(sql, (mid, uid))
        print(effect_row)
        return jsonify({'code': 0, 'msg': 'succeed'})


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
    app.run(host='127.0.0.1', debug=True)

# 没有权限认证
