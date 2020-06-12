# -*- coding: utf-8 -*-
import datetime
import re
import urllib.parse

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinterInfo, QPrinter
import sys, base64
from PyQt5.QtWidgets import QApplication


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
            print(str(item.printerName()))
            if str(self.p) == str(item.printerName()):
                self.printer = QPrinter(item)
                break

    def printing(self):
        print("进入打印方法")
        try:
            if self.printer is None:
                print("当前打印机未选中")
                return

            print("当前打印机是："+str(self.printer))
            p = self.printer
            print("获取到doc")
            doc = QTextDocument()
            doc.setDocumentMargin(0)
            self.log.write(Printer.getTime() + "--physicalDpiX --" + str(p.physicalDpiX()) + "\n")
            print('physicalDpiX:' + str(p.physicalDpiX()))
            print('resolution:' + str(p.resolution()))
            self.log.write(Printer.getTime() + "--resolution --" + str(p.resolution()) + "\n")
            print('height:' + str(p.height()))
            self.log.write(Printer.getTime() + "--height --" + str(p.height()) + "\n")
            print('width:' + str(p.width()))
            self.log.write(Printer.getTime() + "--width --" + str(p.width()) + "\n")
            scale = round(p.physicalDpiX() / p.resolution(), 4)
            print('scale:' + str(scale))
            self.log.write(Printer.getTime() + "--scale --" + str(scale) + "\n")
            print('supportedResolutions:' + str(p.supportedResolutions()))
            self.log.write(Printer.getTime() + "--supportedResolutions --" + str(p.supportedResolutions()) + "\n")
            print('logicalDpiX:' + str(p.logicalDpiX()))
            self.log.write(Printer.getTime() + "--logicalDpiX --" + str(p.logicalDpiX()) + "\n")
            doc.setPageSize(
                QSizeF(p.logicalDpiX() * (p.width() / 25.4 / scale),
                       p.logicalDpiY() * (p.height() / 25.4 / scale)))
            splitHitm = self.getSplitHtml()
            for html in splitHitm:
                self.log.write(Printer.getTime() + "--starting print -- \n")
                print("starting print")
                doc.setHtml(html)
                doc.print_(p)
            doc.clear()
            print("ending print")
            self.log.write(Printer.getTime() + "--end print -- \n")
        except Exception as ee:
            print(str(ee))
            self.log.write(Printer.getTime() + "***print - error****" + str(ee) + "\n")
            self.log.close()

    def closeLog(self):
        self.log.close()
        self.app.flush()
        self.app.quit()

    def __init__(self, name, htmls):
        print(str(sys.argv[0]))
        self.app = QApplication(sys.argv)

        self.log = open(
            str(sys.argv[0]).rsplit("/", 1)[0] + "\RYBPRINTING" + datetime.datetime.now().strftime('%Y-%m') + ".log",
            "a")
        self.p = '空'
        self.html = '空'
        self.printer = None
        if len(htmls) > 0:
            self.p = base64.b64decode(urllib.parse.unquote(Printer.removeHead(name))).decode(
                "utf-8")  # 打印机名称
            print("期望调用打印机：" + self.p)
            self.log.write(Printer.getTime() + "--printer --" + self.p + "\n")
            self.html = base64.b64decode(htmls).decode("utf-8")
            print(self.html)
            self.log.write(Printer.getTime() + "--after decode html --" + self.html + "\n")
            self.getPrinter()
