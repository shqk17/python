# -*- coding:utf-8 -*-

import asyncio
import base64
import ctypes
import datetime
import os
import re
import time
import urllib.parse
import win32event
import win32service

import websockets
import win32serviceutil
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinterInfo, QPrinter
from PyQt5.QtWidgets import QApplication
from appdirs import unicode


def print_ts(message):
    return "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message)


# 检测客户端权限，用户名密码通过才能退出循环
class Printer(object):

    @staticmethod
    def getTime():
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return nowTime

    @staticmethod
    def removeHead(text):
        u = "rybprinting://"
        pattern = re.compile(r'rybprinting://')
        if re.findall(pattern, str(text)):
            text = str(text).replace(u, '')
        return text

    def getPrinterList(self):
        printer = []
        printerInfo = QPrinterInfo()
        for item in printerInfo.availablePrinters():
            printer.append(item.printerName())
            self.log.write(Printer.getTime() + "--availablePrinterName --" + str(item.printerName()))
        return str.join(",", printer)

    def getSplitHtml(self):
        pattern = re.compile(r'<html>(.+?)</html>')
        dd = re.findall(pattern, str(self.html))
        return dd

    def getPrinter(self):
        printerInfo = QPrinterInfo()
        for item in printerInfo.availablePrinters():
            if str(self.p) == str(item.printerName()):
                self.printer = QPrinter(item)
                break

    def printing(self):
        try:
            if self.printer is None:
                return

            p = self.printer
            doc = QTextDocument()
            doc.setDocumentMargin(0)
            self.log.write(Printer.getTime() + "--physicalDpiX --" + str(p.physicalDpiX()) + "\n")
            self.log.write(Printer.getTime() + "--resolution --" + str(p.resolution()) + "\n")
            self.log.write(Printer.getTime() + "--height --" + str(p.height()) + "\n")
            self.log.write(Printer.getTime() + "--width --" + str(p.width()) + "\n")
            scale = round(p.physicalDpiX() / p.resolution(), 4)
            self.log.write(Printer.getTime() + "--scale --" + str(scale) + "\n")
            self.log.write(Printer.getTime() + "--supportedResolutions --" + str(p.supportedResolutions()) + "\n")
            self.log.write(Printer.getTime() + "--logicalDpiX --" + str(p.logicalDpiX()) + "\n")
            doc.setPageSize(
                QSizeF(p.logicalDpiX() * (p.width() / 25.4 / scale),
                       p.logicalDpiY() * (p.height() / 25.4 / scale)))
            splitHitm = self.getSplitHtml()
            for html in splitHitm:
                self.log.write(Printer.getTime() + "--starting print -- \n")
                doc.setHtml(html)
                doc.print_(p)
            doc.clear()
            self.log.write(Printer.getTime() + "--end print -- \n")
        except Exception as ee:
            self.log.write(Printer.getTime() + "***print - error****" + str(ee) + "\n")
            self.log.close()

    def closeLog(self):
        self.log.close()
        self.app.flush()
        self.app.quit()

    def __init__(self, name, htmls):
        self.app = QApplication(sys.argv)
        self.log = open(
            "./" + datetime.datetime.now().strftime('%Y-%m') + ".log",
            "a")
        self.p = '空'
        self.html = '空'
        self.printer = None
        if len(htmls) > 0:
            self.p = base64.b64decode(urllib.parse.unquote(Printer.removeHead(name))).decode(
                "utf-8")  # 打印机名称
            self.log.write(Printer.getTime() + "--printer --" + self.p + "\n")
            self.html = base64.b64decode(htmls).decode("utf-8")
            self.log.write(Printer.getTime() + "--after decode html --" + self.html + "\n")
            self.getPrinter()


class MySocket(object):

    async def check_permit(self, websocket):
        while True:
            recv_str = await websocket.recv()
            cred_dict = recv_str.split(";")
            # 密码可以使用 非对称加密 后期完善
            if cred_dict[0] == "admin" and cred_dict[1] == "123456":
                await websocket.send('{"type":"success"}')
                return True
            else:
                response_str = '{"type":"fail"}'
                await websocket.send(response_str)

    async def recv_msg(self, websocket):
        while True:
            try:
                if (websocket._connection_lost) is True:
                    break

                recv_text = await websocket.recv()
                if not recv_text:
                    continue
                # 或者
                if len(recv_text) == 0:
                    continue
                cred_dict = recv_text.split(";")
                if (len(cred_dict) == 1 and cred_dict[0] == '1'):
                    # 打印列表
                    printer = Printer('', '')
                    printName = printer.getPrinterList()
                    printer.closeLog()
                    await websocket.send('{"type":"1","data":"' + str(printName) + '"}')
                elif len(cred_dict) == 3 and cred_dict[0] == '2':
                    # 打印
                    printerName = cred_dict[1]
                    htmlBase64 = cred_dict[2]
                    printer2 = Printer(printerName, htmlBase64)
                    printer2.printing()
                    printer2.closeLog()
                    await websocket.send('{"type":"打印结束"}')
            except Exception as ee:
                break

    # 服务器端主逻辑
    async def main_logic(self, websocket, path):
        await self.check_permit(websocket)
        await self.recv_msg(websocket)

    def isRunning(self):
        return self.loop.is_running()

    def close(self):
        self.close()

    def restart(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(websockets.serve(self.main_logic, '127.0.0.1', 6892))
        self.loop.run_forever()

    def running(self):
        self.loop.run_until_complete(websockets.serve(self.main_logic, '127.0.0.1', 6892))
        self.loop.run_forever()

    def __init__(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.loop = asyncio.get_event_loop()
        # self.running()
        # t = threading.Thread(target=self.running())  # 创建线程，如果函数里面有参数，args=()
        # t.start()  # 开启线程


def write():
    pid = os.getpid()
    with open('./pid.txt', 'w') as f:
        f.write(str(pid))


def read():
    if os.path.exists('./pid.txt'):
        with open('./pid.txt', 'r')as f:
            pid = f.read()
            return pid
    else:
        return '0'


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# windows服务中显示的名字
class zlsService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'ryb_printer'  ###可以根据自己喜好修改
    _svc_display_name_ = 'ryb_printer'  ###可以根据自己喜好修改
    _svc_description_ = 'ryb_printer'  ###可以根据自己喜好修改

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.run = True

    def SvcDoRun(self):
        # 这里是你的启动代码，由于我的是flask框架程序，只需要把我的主文件from过来即可。
        socket = MySocket()
        socket.running()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        self.run = False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == '__main__':

    import sys
    import servicemanager

    s = open(
        "./" + datetime.datetime.now().strftime('%Y-%m') + ".log",
        "a")
    try:
        if len(sys.argv) == 1:
            try:
                evtsrc_dll = os.path.abspath(servicemanager.__file__)
                servicemanager.PrepareToHostSingle(zlsService)  # 如果修改过名字，名字要统一
                servicemanager.Initialize('ryb_printer', evtsrc_dll)  # 如果修改过名字，名字要统一
                servicemanager.StartServiceCtrlDispatcher()
            except win32service.error as details:
                import winerror

                s.write(str(details))
                s.close()
                if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                    win32serviceutil.usage()
        else:
            win32serviceutil.HandleCommandLine(zlsService)
    except Exception as ee:
        s.write(str(ee))
        s.close()
