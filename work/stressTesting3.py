import threading
import datetime
import requests
from time import sleep, ctime
import re

lock = threading.Lock()
loops = [4, 2]
times = []
error = []


def loop(nloop, nsec, cookie, urlstr):
    # lock.acquire()
    print('start loop ' + str(nloop) + ' at : ' + str(ctime()))
    url = "http://www.zshom.com/webskill/newestNote?page=1&limit=8&dynamicTypeCur=0" + urlstr
    headers = {'Host': 'www.zshom.com',
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
    for j in range(10000):
        try:
            # r = requests.post(url=url, headers=headers, data=data)
            r = requests.get(url=url, headers=headers)
            ResponseTime = float(r.elapsed.microseconds) / 1000
            times.append(ResponseTime)
            if r.status_code != 200:
                error.append("0")
            else:
                print("查询列表成功:" + str(r.text))
        except Exception as e:
            error.append("0")
            print("*****发生异常*****")
        sleep(nsec)
        print('loop ', nloop, ' done at : ', ctime(), '次数：', j + 1)


def main():
    print('starting at : ', ctime())
    urlstr = input("请输入请求接口：")
    cookie = input("请输入cookie：")
    threadsNum = input("请输入执行线程数：")
    thinkTime = input("请输入睡眠时间：")
    starttime = datetime.datetime.now()
    nub = int(threadsNum)
    ThinkTime = float(thinkTime)

    threads = []
    # nloops = range(len(loops))
    nloops = range(nub)

    for i in nloops:
        t = threading.Thread(target=loop, args=(i, ThinkTime, cookie, urlstr))
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
    print('all DONE at : ', ctime())


if __name__ == '__main__':
    main()
