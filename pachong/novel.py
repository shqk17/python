# -*- coding:utf-8 -*-
from time import sleep
import collections
import requests
from bs4 import BeautifulSoup
import os
import threading


def get_zj(j):
    i = 0
    while True:
        if i > 2:
            break
        else:
            try:
                q.pop()
            except:
                i = i + 1
                print("队列已经空了.")
                sleep(1)
                continue
            task = q.popleft()
            url = str(task).split(";")[2]
            print("---当前是----" + str(j) + "------线程任务---------")
            print(url)
            print(str(task).split(";")[1])
            print("-------------------------------")
            try:
                # 访问该章节详情网址，爬取该章节正文
                chapter_req = requests.get(url=url)
                chapter_req.encoding = 'gbk'
                chapter_soup = BeautifulSoup(chapter_req.text, "html.parser")
                # 解析出来正文所在的标签
                content_tag = chapter_soup.div.find(id="content")
                if content_tag is None:
                    content_tag = chapter_soup.find(name="div", attrs={"class": "showtxt"})
                # 获取正文文本，并将空格替换为换行符
                content_text = str(content_tag.text.replace('\xa0', '\n'))
                all_novel[str(task).split(";")[0]] = str(task).split(";")[1] + "\n" + content_text
            except Exception as e:
                print("请求链接失败" + str(e))
                q.append(task)


if __name__ == '__main__':
    # 所要爬取的小说主页，每次使用时，修改该网址即可，同时保证本地保存根路径存在即可
    # 本地保存爬取的文本根路径
    save_path = 'E:\pythonDown'
    # 笔趣阁网站根路径
    # target = "https://www.biqubao.com/book/25397/"
    # index_path = 'https://www.biqubao.com/'
    target = "https://www.23wx.so/20_20732/"
    index_path = 'https://www.23wx.so/20_20732/'
    req = requests.get(url=target)
    # 查看request默认的编码，发现与网站response不符，改为网站使用的gdk
    print(req.encoding)
    req.encoding = 'gbk'
    # 解析html
    soup = BeautifulSoup(req.text, "html.parser")
    list_tag = soup.div(id="list")
    if len(list_tag) < 1:
        list_tag = soup.findAll(name="div", attrs={"id": "list"})
    print('list_tag:', list_tag)
    # 获取小说名称
    story_title = list_tag[0].dl.dt.string
    # 根据小说名称创建一个文件夹,如果不存在就新建
    dir_path = save_path + '/' + story_title
    if not os.path.exists(dir_path):
        os.path.join(save_path, story_title)
        os.mkdir(dir_path)
    # 开始循环每一个章节，获取章节名称，与章节对应的网址

    q = collections.deque()
    num = 0
    for dd_tag in list_tag[0].dl.find_all('dd'):
        num = num + 1
        # 章节名称
        chapter_name = dd_tag.string
        # 章节网址
        try:
            chapter_url = index_path + dd_tag.a.get('href')
        except:
            continue
        # novelList[str(dd_tag.a.get('href')).split("/")[-1].split(".")[0]] = chapter_name + ';' + chapter_url
        print(str(dd_tag.a.get('href')).split("/")[-1].split(".")[0])
        print(chapter_name + ';' + chapter_url)
        q.append(str(dd_tag.a.get('href')).split("/")[-1].split(".")[0] + ';' + chapter_name + ';' + chapter_url)

    print("一共_____:" + str(num))
    threads = []

    all_novel = {}

    for i in range(0, 6):
        t = threading.Thread(target=get_zj, args=(i,))
        threads.append(t)
        t.start()

    for j in threads:
        j.join()

    print("********所有线程执行完毕************")
    novel = sorted(all_novel.items(), key=lambda x: x[0])
    txt = open(dir_path + '/' + story_title + '.txt', 'a', encoding="utf-8")
    for a in novel:
        # 将当前章节，写入以章节名字命名的txt文件
        txt.write(a[1])
        txt.write('\n')
    txt.close()
