# -*- coding:utf-8 -*-

from flask import Flask,request,jsonify,send_from_directory,make_response
import json
import os
import pymysql


path = "http:111.230.153.254/large"
conn = pymysql.connect(host='111.230.153.254',port=3306,user='stickers', passwd='stickers', db='stickers',charset='utf8')
cursor = conn.cursor()
cursor.execute("select VERSION()")
data = cursor.fetchone()
print ("database version : %s" % data)

def table_s_c():
    with open('data.json', 'r') as f:
        data = json.load(f)
    for dict in data:
        folder = dict['folder']
        category = dict['category']
        filenames = dict['meme']
        # try:
        cursor.execute("SELECT * FROM categories WHERE category = %s", (category))
        if cursor.rowcount == 0:
            print('ss')
            cursor.execute("INSERT INTO categories (category, folder) VALUES (%s, %s)", (category, folder))
            cursor.connection.commit()
        # except:
        #     print("sql error")
        #     print(dict)
        #     print('c')
        #     db.rollback()
        for filename in filenames:
            url = os.path.join(path, folder, filename)
            # try:
            cursor.execute("SELECT * FROM stickers WHERE filename = %s", (filename))
            if cursor.rowcount == 0:
                cursor.execute("INSERT INTO stickers (url, category, filename) VALUES (%s, %s, %s)", (url, category, filename))
                cursor.connection.commit()
            # except:
            #     print("sql error")
            #     print(dict)
            #     print('s')
            #     db.rollback()

def table_b():
    sql = 'SELECT sid,category FROM stickers'
    cursor.execute(sql)
    resultall = cursor.fetchall()
    print(resultall)
    conn.commit()
    for item in resultall:
        sid= item[0]
        category = item[1]
        print(category)
        cursor.execute("SELECT * FROM categories WHERE category  = %s", (category))
        if cursor.rowcount == 0:
            print('0') 
        result = cursor.fetchall()
        print(result)
        for it in result:
            cid = it[0]
            cursor.execute("INSERT INTO belong (sid, cid) VALUES (%s, %s)", (sid, cid))
            cursor.connection.commit()

def main():
    # table_b()
    cursor.execute("SELECT * FROM stickers WHERE category  = %s", ('猫眼三姐妹'))
    result = cursor.fetchall()
    print(result)
    for it in result:
        cid = it[0]
    print(cid)
    # cursor.execute("INSERT INTO belong (sid, cid) VALUES (%s, %s)", (sid, cid))
    # cursor.connection.commit()
    conn.close()
    

if __name__ == "__main__":
    main()

     
