# coding:utf-8
import os
import time
from multiprocessing import *


def func():
    print("子进程开始.")
    time.sleep(2)
    print("子进程结束.")


if __name__ == '__main__':
    p = Process(target=func)
    p.daemon = True
    p.start()
    print("主进程结束.")
