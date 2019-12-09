# -*- coding:utf-8 -*-

import json
import os
import pymysql


conn = pymysql.connect(host='111.230.153.254', port=3306, user='stickers', passwd='stickers', db='stickers', charset='utf8')
cursor = conn.cursor()


def insert_categories_stickers():
    path = "http:111.230.153.254/large"
    count = 0
    with open('data.json', 'r') as f:
        data = json.load(f)
    for dict in data:
        folder = dict['folder']
        category = dict['category']
        filenames = dict['meme']
        cursor.execute("SELECT * FROM categories WHERE category = %s", category)
        if cursor.rowcount == 0:
            count += 1
            print(count)
            cursor.execute("INSERT INTO categories (category, folder) VALUES (%s, %s)", (category, folder))
            cursor.connection.commit()
        for filename in filenames:
            url = os.path.join(path, folder, filename)
            cursor.execute("SELECT * FROM stickers WHERE filename = %s", filename)
            if cursor.rowcount == 0:
                cursor.execute("INSERT INTO stickers (url, category, filename) VALUES (%s, %s, %s)", (url, category, filename))
                cursor.connection.commit()
            # try:
            #
            # except:
            #     db.rollback()


def insert_belong():
    sql = 'SELECT sid,category FROM stickers'
    cursor.execute(sql)
    resultall = cursor.fetchall()
    print(resultall)
    conn.commit()
    for item in resultall:
        sid = item[0]
        category = item[1]
        print(category)
        cursor.execute("SELECT * FROM categories WHERE category  = %s", category)
        if cursor.rowcount == 0:
            print('0') 
        result = cursor.fetchall()
        print(result)
        for it in result:
            cid = it[0]
            cursor.execute("INSERT INTO belong (sid, cid) VALUES (%s, %s)", (sid, cid))
            cursor.connection.commit()


def update_url_stickers():
    sql = 'SELECT sid,filename,category FROM stickers'
    cursor.execute(sql)
    resultall = cursor.fetchall()
    conn.commit()
    for item in resultall:
        sid = item[0]
        filename = item[1]
        category = item[2]
        print(filename)
        cursor.execute("SELECT folder2 FROM categories WHERE category  = %s", category)
        result = cursor.fetchall()
        it = result[0]
        folder2 = it[0]
        url = 'http://111.230.153.254/large/' + folder2 + '/' + filename
        print(url)
        cursor.execute("UPDATE stickers SET url =%s WHERE sid  = %s", (url, sid))
        cursor.connection.commit()


def rename_folder():
    sql = 'SELECT folder,folder2 FROM categories'
    cursor.execute(sql)
    resultall = cursor.fetchall()
    conn.commit()
    for item in resultall:
        folder1 = item[0]
        folder2 = item[1]
        path = os.getcwd()
        os.rename(os.path.join(path, 'ChineseBQB', folder1), os.path.join(path, 'ChineseBQB', folder2))


def insert_temps():

    with open('data_temp.json', 'r') as f:
        temps = json.load(f)
    for index, temp in enumerate(temps):
        filename = temp['filename']
        cursor.execute('INSERT INTO templates (filename) VALUES (%s)', filename)
        print(index)
    cursor.connection.commit()


def updat_url_temps():
    sql = 'SELECT tid,filename FROM templates'
    cursor.execute(sql)
    resultall = cursor.fetchall()
    conn.commit()
    for item in resultall:
        tid = item[0]
        filename = item[1]
        print(tid)
        print(filename)

        url = 'http://111.230.153.254/large/' + 'temps' + '/' + filename
        print(url)
        cursor.execute("UPDATE templates SET url =%s WHERE tid  = %s", (url, tid))
    cursor.connection.commit()


def updat_title_temps():
    with open('data_title.json', 'r', encoding='utf-8') as f:
        temps = json.load(f)
    for index, temp in enumerate(temps):
        filename = temp['filename']
        title = temp['title']
        print(filename)
        print(title)
        print(index)
        cursor.execute("UPDATE templates SET title = %s WHERE filename  = %s", (title, filename))
    cursor.connection.commit()


def version():
    cursor.execute("select VERSION()")
    data = cursor.fetchone()
    print("database version : %s" % data)


def main():
    version()
    updat_title_temps()
    cursor.close()
    conn.close()
    

if __name__ == "__main__":
    main()
