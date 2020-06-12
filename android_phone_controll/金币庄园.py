import time

from appium import webdriver


class MyTests():
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
        y1 = int(self.yzb * 0.75)  # 起始y坐标
        y2 = int(self.yzb * 0.25)  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    def swipLeft(self, t, h):
        x1 = int(self.xzb * 0.99)
        y1 = int(self.yzb * h)
        x2 = int(self.xzb * 0.60)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 测试结束后执行的方法
    def tearDown(self):
        self.driver.quit()

    def tap(self, x, y):
        self.driver.tap([(x, y)])

    def guangdian(self, x, y, t):
        # 点击逛店活动
        self.tap(x, y)
        time.sleep(3)
        # 上滑
        self.swipeUp(500, 0.55)  # 1080 宽
        print("上滑")
        for j in range(0, t):
            print("浏览中：" + str(j))
            time.sleep(1)
        # 左滑返回
        self.swipLeft(500, 0.55)
        print("左滑返回")

    def JRRW(self):
        self.tap(115, 1171)
        time.sleep(2)
        # 进入今日任务页面
        # 浏览每日活动
        self.guangdian(956, 998, 11)
        time.sleep(2)
        # 浏览聚划算
        self.guangdian(932, 1213, 11)
        time.sleep(2)
        # 搜索商品
        self.sousuo()
        time.sleep(1)
        # 去首页
        self.tap(932, 1896)
        for j in (0, 11):
            print("浏览中：" + str(j))
            time.sleep(1)

        self.tap(130, 2187)
        time.sleep(1)
        mttest.start(557, 956)
        print("今日任务结束")

    def sousuo(self):
        self.tap(932, 1675)
        time.sleep(2)
        self.tap(819, 1068)
        time.sleep(2)
        for j in range(0, 11):
            print("浏览中：" + str(j))
            time.sleep(1)
        # 左滑返回
        self.swipLeft(500, 0.55)
        print("左滑返回")
        time.sleep(2)
        self.swipLeft(500, 0.55)
        print("左滑返回")
        time.sleep(2)
        self.swipLeft(500, 0.55)
        print("左滑返回")

    def start(self, x, y):
        self.tap(x, y)
        time.sleep(2)
        self.tap(152, 475)
        time.sleep(2)

    def Lfeiliao(self):
        self.tap(975, 1138)
        time.sleep(1)
        #每日打卡

        #逛 1
        self.guangdian(899, 1166, 21)
        time.sleep(2)

        # 逛 2
        self.guangdian(899, 1380, 21)
        time.sleep(2)

        # 逛 3
        self.guangdian(899, 1600, 21)
        time.sleep(2)
        # 逛 4
        self.guangdian(899, 1800, 21)
        time.sleep(2)
        # 逛 5
        self.guangdian(899, 2020, 21)
        time.sleep(2)
        # # 上滑
        # self.swipeUp(500, 0.55)  # 1080 宽
        # print("上滑")
        # time.sleep(2)
        # # 逛 6
        # self.guangdian(899, 1860, 21)
        # time.sleep(2)
        # # 逛 7
        # self.guangdian(899, 2080, 21)
        # time.sleep(2)
        #关闭
        self.tap(1019, 566)



if __name__ == "__main__":
    print("开始测试")
    mttest = MyTests()
    mttest.getSize()
    mttest.start(557, 956)
    # 今日任务
    # mttest.JRRW()
    # 领肥料
    mttest.Lfeiliao()
    #
    mttest.tearDown()
    print("结束")
