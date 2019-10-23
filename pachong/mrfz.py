# -*- coding:utf-8 -*-
from time import sleep
import collections
import requests
from bs4 import BeautifulSoup
import uuid
import re
import datetime
import queue

from pachong.bsUtil import getDBLink


def get_hero_info(ejz, name):
    url = detalInfoUrl + ("title=%s&action=edit" % ejz)

    try:
        chapter_req = requests.get(url=url)
        chapter_req.encoding = 'utf-8'
        chapter_soup = BeautifulSoup(chapter_req.text, "html.parser")
        content_tag = chapter_soup.find(name="textarea", attrs={"id": "wpTextbox1"})

        str(content_tag.text)
        pattern_job = re.search('(\|职业=)(.+?)\n', str(content_tag.text))
        job = pattern_job.group(2)
        pattern_stars = re.search('(\|星级=)(.+?)\n', str(content_tag.text))
        stars = pattern_stars.group(2)
        pattern_tag = re.search('(\|标签=)(.+?)\n', str(content_tag.text))
        tag = pattern_tag.group(2)
        pattern_sex = re.search('(\|性别=)(.+?)\n', str(content_tag.text))
        sex = pattern_sex.group(2)
        place = tag.split("、")[0]
        return job, stars, tag, sex, place
    except Exception as e:
        print(e)
        return None, None, None, None, None


if __name__ == '__main__':
    save_path = './'

    target = "http://wiki.joyme.com/arknights/公开招募工具"
    index_path = 'http://wiki.joyme.com/arknights'
    req = requests.get(url=target)
    print(req.encoding)
    req.encoding = 'utf-8'
    # 解析html
    soup = BeautifulSoup(req.text, "html.parser")
    list_tag = soup.findAll(name="div", attrs={"class": "contentDetail"})
    detalInfoUrl = "http://wiki.joyme.com/arknights/index.php?"
    # detalInfoUrl = "http://wiki.joyme.com/arknights/?"
    hero_info = {}
    for i in list_tag:
        erjz_name = str(i.p.a.get('href')).split("/")[2]
        hero_name = str(i.p.a.get('title'))
        hero_head = str(i.p.a.img.get('src'))
        hero_info[erjz_name] = hero_name + "," + hero_head

    insetSql = "INSERT INTO `mrfz_db`.`hero_base_info` (`id`," \
               " `name`, " \
               "`avatarUrl`," \
               " `stars`, " \
               "`job`, `sex`," \
               " `place`, `tag`, `createTime`)" \
               " VALUES ('%s'," \
               " '%s'," \
               " '%s', " \
               "'%d'," \
               " '%s'," \
               " %d," \
               " '%s'," \
               " '%s'," \
               " '%s');"
    cursor, db = getDBLink(1)
    for k, v in hero_info.items():
        job, stars, tag, sex, place = get_hero_info(k, v.split(",")[0])
        print(v.split(",")[0])
        if job is None:
            print("******该英雄爬取失败*******")
            continue
        sex_num = 0
        if sex == '男':
            sex_num = 1

        inset_sql = insetSql % (str(uuid.uuid4()).replace("-", ""),
                                str(v.split(",")[0]),
                                str(v.split(",")[1]),
                                int(stars),
                                str(job),
                                sex_num,
                                str(place),
                                str(tag), str(datetime.datetime.now()).split(".")[0])
        print(inset_sql)
        cursor.execute(inset_sql)
    db.commit()
    db.close()
