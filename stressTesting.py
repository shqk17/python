import requests
import datetime
import time
import threading

cookie = ""
duanyan = ""
threadsNum = 1
thinkTime = 1


class sendRequest():
    times = []
    error = []

    def requset(self, cookie, duanyan):
        mytest = sendRequest
        url = "http://192.168.0.4:8080/tss/tssMemberPackageController/tssMemberPackageList.do"
        headers = {'Host': '192.168.0.4:8081',
                   'Connection': 'keep-alive',
                   'Cache-Control': 'max-age=0',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate',
                   # 'Cookie': 'navbar-fixed-top=true; sidebar-fixed=true; breadcrumbs-fixed=true; page-header-fixed=false; page-header-isShow=false; Hm_lvt_25437122cff4baad62984b1f218a0b02=1551334603,1551671508,1551679939,1551681634; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=undefined; SL_wptGlobTipTmp=undefined; JSESSIONID=8DE1896FD5C66F9B592995C63AB83671; Hm_lpvt_25437122cff4baad62984b1f218a0b02=1551784723',
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
            mytest.times.append(ResponseTime)
            if r.status_code != 200:
                mytest.error.append("0")
            # 定义断言ID
            # ss = 'ff8080816947a871016947eee24c0646'
            ss = duanyan
            htmlss = str(r.text).replace("\r", "").strip()
            if ss in htmlss:
                print("---断言成功_" + str(datetime.datetime.now()) + "---")
                mytest.error.append("1")
            else:
                mytest.error.append("2")
                print("---断言失败_" + str(datetime.datetime.now()) + "---")
                flieLog = open("./11.txt", "a")
                flieLog.write(r.text)
                flieLog.close()
        except Exception as e:
            mytest.error.append("0")
            print("*****发生异常*****")
            flieLog = open("./error.txt", "a")
            flieLog.write(str(e))
            flieLog.close()


if __name__ == "__main__":
    mytest = sendRequest()

    cookie = input("请输入cookie：")
    duanyan = input("请输入断言字符串：")
    threadsNum = input("请输入执行线程数：")
    thinkTime = input("请输入睡眠时间：")

    threads = []
    starttime = datetime.datetime.now()
    print("request start time %s " % starttime)
    nub = int(threadsNum)
    ThinkTime = float(thinkTime)
    for i in range(1, nub + 1):
        try:
            t = threading.Thread(target=mytest.requset(cookie, duanyan), args='')
            threads.append(t)
        except Exception as e:
            pass
    for t in threads:
        print("睡眠"+str(2)+"秒:"+str(datetime.datetime.now()))
        time.sleep(2)
        print("睡眠" + str(2) + "秒"+str(datetime.datetime.now()))
        t.setDaemon(True)
        t.start()
        t.join()
    endtime = datetime.datetime.now()
    print("request end time %s" % endtime)
    time.sleep(0.1)
    AverageTime = "{:.3f}".format(float(sum(mytest.times)) / float(len(mytest.times)))
    print("Average Response Time %s ms" % AverageTime)
    usertime = str(endtime - starttime)
    hour = usertime.split(':').pop(0)
    minute = usertime.split(':').pop(1)
    second = usertime.split(':').pop(2)
    totaltime = float(hour) * 60 * 60 + float(minute) * 60 + float(second)
    print("Concurrent processing %s" % nub)
    print("use total time %s s" % (totaltime - float(nub * ThinkTime)))
    print("异常统计 request %s" % mytest.error.count("0"))
    print("断言失败统计 request %s" % mytest.error.count("2"))
    print("断言成功统计 request %s" % mytest.error.count("1"))
