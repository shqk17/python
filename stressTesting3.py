import threading
import datetime
import requests
from time import sleep, ctime
import tkinter as tk
from tkinter import *
import re

lock = threading.Lock()
loops = [4, 2]
times = []
error = []


def loop(nloop, nsec, cookie, duanyan, urlstr):
    lock.acquire()
    print('start loop ' + str(nloop) + ' at : ' + str(ctime()))
    url = "http://192.168.0.4:8080/tss/" + urlstr
    headers = {'Host': '192.168.0.4:8081',
               'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8'
               }

    data = {
        'type': '1',
        'pageSize': '15'
    }
    # 设置cookies：
    headers['Cookie'] = cookie
    try:
        r = requests.post(url=url, headers=headers, data=data)
        ResponseTime = float(r.elapsed.microseconds) / 1000
        times.append(ResponseTime)
        if r.status_code != 200:
            error.append("0")
        # 定义断言ID
        ss = duanyan
        htmlss = str(r.text).replace("\r", "").strip()
        if ss in htmlss:
            print("---断言成功_" + str(datetime.datetime.now()) + "---")
            error.append("1")
        else:
            error.append("2")
            print("---断言失败_" + str(datetime.datetime.now()) + "---")
            flieLog = open("./11.txt", "a")
            flieLog.write(r.text)
            flieLog.close()
    except Exception as e:
        error.append("0")
        print("*****发生异常*****")
        flieLog = open("./error.txt", "a")
        flieLog.write(str(e))
        flieLog.close()
    lock.release()
    sleep(nsec)
    print('loop ', nloop, ' done at : ', ctime())


def main():
    root = tk.Tk()  # 这里
    # fix the root window size
    # root.minsize(920, 750)
    # root.maxsize(920, 750)  # 这里主要是控制窗口的大小，让窗口大小不能改变
    # root.geometry("1366x250")
    root.title('SQL转换工具_by enAries')  # 设置主窗口的标题
    # display the quit button
    text = edit(root)  #
    l = tk.Label(root, text='压力测试工具', fg='white', bg='black', width=100)
    l.grid(row=4, column=0, columnspan=5, sticky=tk.E + tk.W + tk.S + tk.N)
    button(root, text)
    # quitbutton(root)
    root.mainloop()  # 这里进入顶层窗口的循环

    print('starting at : ', ctime())
    urlstr = input("请输入请求接口：")
    cookie = input("请输入cookie：")
    duanyan = input("请输入断言字符串：")
    threadsNum = input("请输入执行线程数：")
    thinkTime = input("请输入睡眠时间：")
    starttime = datetime.datetime.now()
    nub = int(threadsNum)
    ThinkTime = float(thinkTime)

    threads = []
    # nloops = range(len(loops))
    nloops = range(nub)

    for i in nloops:
        t = threading.Thread(target=loop, args=(i, ThinkTime, cookie, duanyan, urlstr))
        threads.append(t)

    for i in nloops:
        sleep(ThinkTime)
        threads[i].start()

    for i in nloops:
        threads[i].join()
    endtime = datetime.datetime.now()
    print("request end time %s" % endtime)
    AverageTime = "{:.3f}".format(float(sum(times)) / float(len(times)))
    print("Average Response Time %s ms" % AverageTime)
    usertime = str(endtime - starttime)
    hour = usertime.split(':').pop(0)
    minute = usertime.split(':').pop(1)
    second = usertime.split(':').pop(2)
    totaltime = float(hour) * 60 * 60 + float(minute) * 60 + float(second)
    print("Concurrent processing %s" % nub)
    print("use total time %s s" % (totaltime - float(nub * ThinkTime)))
    print("异常统计 request %s" % error.count("0"))
    print("断言失败统计 request %s" % error.count("2"))
    print("断言成功统计 request %s" % error.count("1"))
    print('all DONE at : ', ctime())


def edit(root):
    lbObejct = Label(root, text="接口地址:")
    lbObejct.grid(row=0, column=0)
    pathObejct = StringVar()
    entryObejct = Entry(root, textvariable=pathObejct)
    entryObejct.grid(row=0, column=1, columnspan=3)
    # 第二行
    lbMsg = Label(root, text="请输入cookie:")
    lbMsg.grid(row=1, column=0)
    pathMsg = StringVar()
    entryMsg = Entry(root, textvariable=pathMsg)
    entryMsg.grid(row=1, column=1, columnspan=3)
    # 第三行
    lbNum = Label(root, text="请输入断言字符串:")
    lbNum.grid(row=2, column=0)
    pathNum = StringVar()
    entryNum = Entry(root, textvariable=pathNum)
    entryNum.grid(row=2, column=1, columnspan=3)
    # 第四行
    urlNum = Label(root, text="请输入执行线程数:")
    urlNum.grid(row=3, column=0)
    pathUrl = StringVar()
    entryUrl = Entry(root, textvariable=pathUrl)
    entryUrl.grid(row=3, column=1, columnspan=3)

    # 第五行
    urlSleep = Label(root, text="请输入睡眠时间:")
    urlSleep.grid(row=4, column=0)
    pathSleep = StringVar()
    entrySleep = Entry(root, textvariable=pathSleep)
    entrySleep.grid(row=4, column=1, columnspan=3)

    result = tk.Text(root, fg='black', bg='#DCDCDC', font='微软雅黑', width=30, height=10, )
    result.grid(row=2, column=0, columnspan=5, sticky=tk.N + tk.E + tk.W)

    # button 传递参数使用lambda函数
    # delete all the value in the text editor
    clear2 = tk.Button(root, text='Clear', width=80, bg='#F5DEB3', font='微软雅黑',
                       command=lambda: ClearAll(result, edit))
    clear2.grid(row=3, column=0, columnspan=5)
    text = [edit, result]
    return text


# 这里定义窗口中所有的按钮控件，并且显示出来，并且设置好每个按钮的响应函数，使用button的command选项来控制
def button(root, text):
    clu = 0
    transformation = tk.Button(root, text='格式化sql', fg='black', width=20, command=lambda: Transformation(text))
    but = [transformation]
    for i in but:
        i.grid(row=1, column=clu, sticky=tk.N + tk.E + tk.W)
        clu += 1
    return but


if __name__ == '__main__':
    main()
