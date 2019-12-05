# -*- coding:utf-8 -*-
import pymysql
from DBUtils.PooledDB import PooledDB

POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,
    # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用。
    # 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host='111.230.153.254',
    port=3306,
    user='stickers',
    password='stickers',
    database='stickers',
    charset='utf8'
)


def execute_all(sql, param=None):
    conn = POOL.connection()
    cursor = conn.cursor()
    try:
        if param:
            cursor.execute(sql, param)
        else:
            cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        cursor.close()
        conn.close()


def execute_eff(sql, param):
    conn = POOL.connection()
    try:
        with conn.cursor() as cursor:
            effect_row = cursor.execute(sql, param)
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
    conn.close()
    return effect_row

