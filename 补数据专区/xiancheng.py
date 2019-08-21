from time import sleep, ctime
import queue, threading


def fenfa(q, contents):
    i = 0
    print("任务开始分发")
    while (True):
        if q.full():
            sleep(1)
            print("分发开始睡眠")
            continue
        q.put(contents[i])
        i = i + 1
        if i >= len(contents):
            print("任务分发完毕")
            break


def createXc(loop, num, q, contents):
    lock = threading.Lock()
    threads = []
    s = threading.Thread(target=fenfa, args=(q, contents ))
    threads.append(s)

    for i in range(num):
        t = threading.Thread(target=loop, args=(i, q ,lock))
        threads.append(t)

    for i in range(num+1):
        threads[i].start()

    for i in range(num+1):
        threads[i].join()
