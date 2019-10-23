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
        x2 = int(self.xzb * 0.50)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 测试结束后执行的方法
    def tearDown(self):
        self.driver.quit()

    def tap(self, x, y):
        self.driver.tap([(x, y)])

    def guangdian(self, x, y):
        # 点击逛店活动
        self.tap(x, y)
        time.sleep(2)
        # 上滑
        self.swipeUp(500, 0.55)  # 1080 宽
        print("上滑")
        for j in range(1, 17):
            print("浏览中：" + str(j))
            time.sleep(1)
        # 左滑返回
        self.swipLeft(500, 0.55)
        print("左滑返回")

    def operateAction(self, flag):
        if flag == 1:
            pass
        elif flag == 2:
            # 逛店活动
            for i in range(1, 20):
                self.guangdian(920, 1280)
                time.sleep(1)
        elif flag == 3:
            for i in range(1, 20):
                self.guangdian(920, 1435.2)
                time.sleep(1)
        elif flag == 4:
            for i in range(1, 20):
                self.guangdian(920, 1590.2)
                time.sleep(1)
        elif flag == 5:
            for i in range(1, 20):
                self.guangdian(920, 1745.2)
                time.sleep(1)
        elif flag == 6:
            for i in range(1, 20):
                self.guangdian(920, 1800)
                time.sleep(1)

if __name__ == "__main__":
    print("开始测试")
    mttest = MyTests()
    mttest.getSize()
    # 点击领猫币 到领猫币中心
    mttest.tap(920, 1640)
    print("进入领币中心了")
    time.sleep(1)
    # 1,全部活动，2逛店活动，3,4,5,6
    mttest.operateAction(5)
    mttest.tearDown()
    print("结束")
