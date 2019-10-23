import time
import unittest

from appium import webdriver


class MyTest():
    def __init__(self):
        desired_caps = {'platformName': 'Android',  # 平台名称
                        # 'platformVersion': '9',  # 系统版本号
                        'deviceName': 'HONOR V20',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
                        }
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)  # 连接Appium
        self.driver.implicitly_wait(8)
        print("初始化成功")

    # 测试开始前执行的方法
    def setUp(self):
        desired_caps = {'platformName': 'Android',  # 平台名称
                        # 'platformVersion': '9',  # 系统版本号
                        'deviceName': 'HONOR V20',  # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
                        }
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)  # 连接Appium
        self.driver.implicitly_wait(8)
        print("初始化成功")

    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        self.xzb = x
        self.yzb = y
        print(x)
        print(y)


    def swipeUp(self, t, w):
        x1 = int(self.xzb * w)  # x坐标
        y1 = int(self.yzb * 0.95)  # 起始y坐标
        y2 = int(self.yzb * 0.01)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    def swipLeft(self, t, h):
        x1 = int(self.xzb * 0.95)
        y1 = int(self.yzb * h)
        x2 = int(self.xzb * 0.01)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 测试结束后执行的方法
    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    print("开始测试")
    mttest = MyTest()
    mttest.getSize()
    mttest.swipeUp(1000, 0.15) #1080 宽  162
    mttest.swipeUp(1000, 0.25) #1080 宽  270
    mttest.swipeUp(1000, 0.35) #1080 宽  378
    mttest.swipeUp(1000, 0.45) #1080 宽  486
    mttest.swipeUp(1000, 0.55) #1080 宽  594
    mttest.swipeUp(1000, 0.65) #1080 宽  702
    mttest.swipeUp(1000, 0.75) #1080 宽  810
    mttest.swipeUp(1000, 0.85) #1080 宽  918
    mttest.swipeUp(1000, 0.95) #1080 宽  1026
    time.sleep(0.5)
    mttest.swipLeft(1000, 0.15) #2208 高 331.2           1
    mttest.swipLeft(1000, 0.20) #2208 高 441.6           2
    mttest.swipLeft(1000, 0.25) #2208 高 552             3
    mttest.swipLeft(1000, 0.30) # 2208 高 662.4          4
    mttest.swipLeft(1000, 0.35) #2208 高 772.8           5
    mttest.swipLeft(1000, 0.40)  # 2208 高 883.2         6
    mttest.swipLeft(1000, 0.45) #2208 高 993.6           7
    mttest.swipLeft(1000, 0.50)  # 2208 高 1104          8
    mttest.swipLeft(1000, 0.55) #2208 高 1214.4          9
    mttest.swipLeft(1000, 0.60)  # 2208 高 1324.8        10
    mttest.swipLeft(1000, 0.65) #2208 高 1435.2          11
    mttest.swipLeft(1000, 0.70)  # 2208 高 1545.6        12
    mttest.swipLeft(1000, 0.75) #2208 高 1656            13
    mttest.swipLeft(1000, 0.80)  # 2208 高 1766.4        14
    mttest.swipLeft(1000, 0.85) #2208 高 1876.8          15
    mttest.swipLeft(1000, 0.90)  # 2208 高 1987.2        16
    mttest.swipLeft(1000, 0.95) #2208 高 2097.6          17
    mttest.tearDown()
