from flask import request,jsonify,current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def create_token(userid):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''

    #参数：私钥 有效期
    s = Serializer(current_app.config["SECRET_KEY"],expires_in=3600)
    #接收用户id转换与编码
    token = s.dumps({"id":userid}).decode("ascii")
    return token

def verify_token(token):
    '''
    校验token
    :param token: 
    :return: 用户信息 or None
    '''
    
    #参数：私有秘钥
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        #转换为字典
        data = s.loads(token)
    except Exception:
        return None
    return data["id"]
    # #拿到转换后的数据，根据模型类去数据库查询用户信息
    # user = User.query.get(data["id"])
    # return user



def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        try:
            #在请求头上拿到token
            token = request.headers["token"]
        except Exception:
            #没接收的到token,给前端抛出错误
            #这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            return jsonify(code = 4103,msg = '缺少参数token')
        
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception:
            return jsonify(code = 4101,msg = "登录已过期")

        return view_func(*args,**kwargs)

    return verify_token