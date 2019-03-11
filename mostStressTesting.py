import threading
import datetime
import requests
import json
import random
from time import sleep, ctime

lock = threading.Lock()
loops = [4, 2]
times = []
error = []


def loop(nloop, nsec, datas, oneuser):
    lock.acquire()
    print('start loop ' + str(nloop) + ' at : ' + str(ctime()))
    url = datas['url']
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }

    data = datas['query']
    # 设置cookies：
    headers['Cookie'] = datas['cookie']
    headers['Host'] = datas['host']
    try:
        r = requests.post(url=url, headers=headers, data=data)
        ResponseTime = float(r.elapsed.microseconds) / 1000
        times.append(ResponseTime)
        if r.status_code != 200:
            error.append("0")
        # 定义断言ID
        ss = datas['duanyan']
        htmlss = str(r.text).replace("\r", "").strip()
        if ss in htmlss:
            print("用户" + str(oneuser) + "---断言成功_" + str(datetime.datetime.now()) + "---")
            error.append("1")
        else:
            error.append("2")
            print("用户" + str(oneuser) + "---断言失败_" + str(datetime.datetime.now()) + "---")
            flieLog = open("./yaliceslog.txt", "a")
            flieLog.write("用户" + str(oneuser) + "-----\n" + r.text)
            flieLog.close()
    except Exception as e:
        error.append("0")
        print("用户" + str(oneuser) + "*****发生异常*****")
        flieLog = open("./error.txt", "a")
        flieLog.write(str(e))
        flieLog.close()
    lock.release()
    sleep(nsec)
    print('loop ', nloop, ' done at : ', ctime())


def main():
    print('starting at : ', ctime())
    flieLog = open("./request_data.txt", "r")
    requestDatas = json.loads(str(flieLog.read()))
    starttime = datetime.datetime.now()
    nub = int(requestDatas['threadsNum'])
    ThinkTime = float(requestDatas['thinkTime'])

    # 用户信息组
    userInfo = {}
    userNum = int(requestDatas['user'])
    for i in range(1, userNum + 1):
        date = requestDatas['data' + str(i)]
        date['url'] = requestDatas['url']
        date['host'] = requestDatas['host']
        userInfo[str(i)] = date
    threads = []
    nloops = range(nub)

    for i in nloops:
        oneuser = random.randint(1, userNum)
        t = threading.Thread(target=loop, args=(i, ThinkTime, userInfo[str(oneuser)], oneuser))
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


if __name__ == '__main__':
    main()
