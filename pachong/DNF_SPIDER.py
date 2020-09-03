# -*- coding:utf-8 -*-
from time import sleep
import collections
import requests
from bs4 import BeautifulSoup
import os
import pymysql
import re
import threading
import urllib.parse

# 全局变量
# 类型目录
title_url = "https://bbs.mdnf.qq.com/forum.php?mod=forumdisplay&fid=38&filter=typeid&typeid=%d&orderby=lastpost&inajax=1&page=%d&mobile=2"
typeids = [18, 19, 20]
host = "https://bbs.mdnf.qq.com/"


def getDb():
    db = pymysql.connect(host='39.98.205.59',
                         port=3306,
                         user='admin',
                         passwd='Aa123456@',
                         db='spider_tb',
                         charset='utf8'
                         , cursorclass=pymysql.cursors.DictCursor
                         )
    return db.cursor(), db


def getTitleDefualt(title_id, title_name, url):
    global host
    try:
        cursor, db = getDb()
        # 查询当前id有没有 没有才继续，有就跳过
        select_sql = "select * from dnf_spider where  id = %d"
        cursor.execute(select_sql % int(title_id))
        result = cursor.fetchall()
        if len(result) > 0:
            print("..............." + str(title_id) + "—" + str(title_name) + "已存在...")
            return
        content_url = host + url
        req = requests.get(url=content_url)
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text, "html.parser")
        content_tag = soup.findAll(name="td", attrs={"class": "t_f"})[0].contents
        haveImge = False
        contents = ""
        for cents in content_tag:
            if str(cents).__contains__("ignore_js_op"):
                haveImge = True
                continue
            contents = contents + cents
        if haveImge:
            imgurl = dict(soup.findAll(name="td", attrs={"class": "t_f"})[0].ignore_js_op.div.img.attrs).get('makefile')
            insert_sql = "insert into dnf_spider (`id`,`title_name`,`title_url`,`content`,`createTime`,`img`)" \
                         " values (%d,'%s','%s','%s','%s','%s')"
            cursor.execute(insert_sql % (
                int(title_id), title_name, content_url, contents, '2020-08-12 12:00:00', imgurl))
        else:
            insert_sql = "insert into dnf_spider (`id`,`title_name`,`title_url`,`content`,`createTime`)" \
                         " values (%d,'%s','%s','%s','%s')"
            cursor.execute(insert_sql % (
                int(title_id), title_name, content_url, contents, '2020-08-12 12:00:00'))

        db.commit()
        cursor.close()
        db.close()
        print("..............." + str(title_id) + "—" + str(title_name) + "存储完毕...")
    except Exception as ee:
        print(str(ee))


def getTitleInfo():
    global title_url, typeids
    for type_id in typeids:
        page_index = 1
        while True:
            try:
                req = requests.get(url=(title_url) % (type_id, page_index))
                page_index = page_index + 1
                print(req.encoding)
                req.encoding = 'utf-8'
                # 解析html
                soup = BeautifulSoup(req.text, "html.parser")
                title_tag = soup.findAll(name="div", attrs={"class": "wbthreadlist_body"})
                if len(title_tag) < 1:
                    break
                for title in title_tag:
                    url_ = dict(title.a.attrs).get("href")
                    title_name = title.span.contents[0]
                    decode_url = urllib.parse.unquote(url_)
                    print(decode_url)
                    pattern_job = re.search('&tid=(.+?)&', str(decode_url))
                    title_id = pattern_job.group(1)
                    getTitleDefualt(title_id, title_name, decode_url)
                if len(title_tag) < 10:
                    break
            except Exception as ee:
                print(str(ee))


if __name__ == '__main__':
    getTitleInfo()
