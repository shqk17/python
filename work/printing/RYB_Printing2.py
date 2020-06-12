# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinterInfo, QPrinter
import urllib.parse, re

from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Printer:

    def __init__(self, p):
        printer = []
        printerInfo = QPrinterInfo()
        print('availablePrinterNames', printerInfo.availablePrinterNames())
        print('defaultPrinterName', printerInfo.defaultPrinterName())
        if p is None or p == "":
            self.p = QPrinterInfo.defaultPrinter()
            self.print_device = QPrinter(self.p)
        else:
            for item in printerInfo.availablePrinters():
                printer.append(item.printerName())
            if p in printer:
                self.p = QPrinter(p)
            else:
                self.p = QPrinterInfo.defaultPrinter()
            self.print_device = QPrinter(self.p)  # 指定打印所使用的装置

    def print(self, content):
        # 设置打印内容的宽度，否则打印内容会变形
        self.print_device.setPageSizeMM(QSizeF(110, 250))
        d = QTextDocument()  # 使用QTextDcument对html进行解析
        font = d.defaultFont()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)
        d.setDefaultFont(font)
        font.setPixelSize(5)
        d.setDocumentMargin(0)  # 将打印的边距设为0
        # d.setHtml(content)  # 注入html内容
        p.setOutputFormat(QPrinter.NativeFormat)
        d.setHtml(u'%s' % content)
        # doc.print_(p)
        d.print(self.print_device)  # 调用打印机进行打印

    def print_new(self, context):
        print("当前打印机：" + str(printer))
        p = self.print_device
        doc = QTextDocument()
        doc.setDocumentMargin(0)
        print('physicalDpiX:' + str(p.physicalDpiX()))
        print('resolution:' + str(p.resolution()))
        print('height:' + str(p.height()))
        print('width:' + str(p.width()))
        scale = p.physicalDpiX() / p.resolution()
        print('scale:' + str(scale))
        print('supportedResolutions:' + str(p.supportedResolutions()))
        print('logicalDpiX:' + str(p.logicalDpiX()))
        doc.setPageSize(
            QSizeF(p.logicalDpiX() * (p.width() / 25.4 / scale),
                   p.logicalDpiY() * (p.height() / 25.4 / scale)))
        doc.setHtml(context)
        print("开始打印")
        p.setOutputFormat(QPrinter.NativeFormat)
        doc.print_(p)

    @staticmethod
    def removeHead(text):
        u = "rybprinting://"
        pattern = re.compile(r'rybprinting://')
        if re.findall(pattern, str(text)):
            text = str(text).replace(u, '')
        return text

    @staticmethod
    def getPrinter(p):
        printer = []
        printerInfo = QPrinterInfo()
        print('availablePrinterNames', printerInfo.availablePrinterNames())
        print('defaultPrinterName', printerInfo.defaultPrinterName())
        for item in printerInfo.availablePrinters():
            printer.append(item.printerName())
        if p in printer:
            print(p)
            return p
        else:
            print(printerInfo.defaultPrinterName())
            return printerInfo.defaultPrinterName()

    def getPrintList(self):
        printer = []
        printerInfo = QPrinterInfo()
        print('availablePrinterNames', printerInfo.availablePrinterNames())
        print('defaultPrinterName', printerInfo.defaultPrinterName())
        for item in printerInfo.availablePrinters():
            printer.append(item.printerName())
        return printer

    @staticmethod
    def printing(printer, context):
        print("当前打印机：" + str(printer))
        printerInfo = QPrinterInfo()
        p = QPrinter()
        for item in printerInfo.availablePrinters():
            if printer == str(item.printerName()):
                p = QPrinter(item)

        doc = QTextDocument()
        doc.setDocumentMargin(0)
        print('physicalDpiX:' + str(p.physicalDpiX()))
        print('resolution:' + str(p.resolution()))
        print('height:' + str(p.height()))
        print('width:' + str(p.width()))
        scale = p.physicalDpiX() / p.resolution()
        print('scale:' + str(scale))
        print('supportedResolutions:' + str(p.supportedResolutions()))
        print('logicalDpiX:' + str(p.logicalDpiX()))
        doc.setPageSize(
            QSizeF(p.logicalDpiX() * (p.width() / 25.4 / scale),
                   p.logicalDpiY() * (p.height() / 25.4 / scale)))
        doc.setHtml(context)
        # new_p = QPrinter()
        print("开始打印")
        p.setOutputFormat(QPrinter.NativeFormat)
        doc.print_(p)


class Print(QObject):
    def __init__(self, p):
        super().__init__()
        self.printer = Printer(p)

    @pyqtSlot(str, result=str)
    def print(self, content):
        self.printer.print_new(content)
        return

    @pyqtSlot(str, result=str)
    def getPrintList(self):
        return self.printer.getPrintList()


if __name__ == '__main__':
    import sys, base64
    from PyQt5.QtWidgets import QApplication

    # 1.打印机(为空，使用默认打印机) 2.html
    # argvStr = sys.argv[1]
    # isJingmo = sys.argv[2]
    argvStr = 0
    isJingmo = 0
    print(argvStr)
    # html = sys.argv[3]
    html = 'PGh0bWw+PHN0eWxlPiNteXNvY2tldFByaW50e2ZvbnQtZmFtaWx5Oiflvq7ova/pm4Xpu5EnLCdNaWNyb3NvZnQgWWFIZWknO2ZvbnQtc2l6ZToxNXB0fS5wcmludC1ib3h7d2lkdGg6MTAwJTttYXJnaW4tdG9wOjIwcHg7bGluZS1oZWlnaHQ6MTJwdH10ZHtmb250LXNpemU6MTVwdH0uY3twYWRkaW5nLWxlZnQ6MjBweH08L3N0eWxlPjxib2R5PjxkaXYgd2lkdGg9IjMwMHB4ImlkPSJteXNvY2tldFByaW50Ij48ZGl2IGNsYXNzPSJwcmludC1ib3giPjxkaXYgYWxpZ249ImNlbnRlciJzdHlsZT0iZm9udC1zaXplOiAyMnB0Owlmb250LXdlaWdodDogNTAwOyI+57qi6buE6JOd5Lqy5a2Q5ZutPC9kaXY+PGRpdiBjbGFzcz0iaHIiPjxiIHN0eWxlPSJmb250LXNpemU6IDIycHQ7Ij4tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS08L2I+PC9kaXY+PGRpdiBhbGlnbj0iY2VudGVyInN0eWxlPSJtYXJnaW4tYm90dG9tOiAzcHg7Ij4yMDE55bm0MTHmnIgyNuaXpTA5OjU0PC9kaXY+PGRpdiBhbGlnbj0iY2VudGVyIj7nrb7liLDlrp3lrp3vvJrjgJDkuo7kvbPkuZDjgJE8L2Rpdj48ZGl2IGNsYXNzPSJociJzdHlsZT0ibWFyZ2luLXRvcDogMjBweDsiPjxiIHN0eWxlPSJmb250LXNpemU6IDIycHQiPi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLTwvYj48L2Rpdj48dGFibGU+PHRyPjx0ZCBjbGFzcz0iYyJhbGlnbj0icmlnaHQiPuivvueoi+WQjeensO+8mjwvdGQ+PHRkIGFsaWduPSJsZWZ0Ij7pn7PkuZBJSTwvdGQ+PC90cj48dHI+PHRkIGNsYXNzPSJjImFsaWduPSJyaWdodCI+5LiK6K++5pe26Ze077yaPC90ZD48dGQgYWxpZ249ImxlZnQiPjExOjUzOjQ1PC90ZD48L3RyPjx0cj48dGQgY2xhc3M9ImMiYWxpZ249InJpZ2h0Ij7mjojor77ogIHluIjvvJo8L3RkPjx0ZCBhbGlnbj0ibGVmdCI+6ICB5biI5LiAZmdmZ2dnPC90ZD48L3RyPjx0cj48dGQgY2xhc3M9ImMiYWxpZ249InJpZ2h0Ij7mtojogJfor77ml7bvvJo8L3RkPjx0ZCBhbGlnbj0ibGVmdCI+MeivvuaXtjwvdGQ+PC90cj48dHI+PHRkIGNsYXNzPSJjImFsaWduPSJyaWdodCI+5raI6ICX6K++5YyF77yaPC90ZD48dGQgYWxpZ249ImxlZnQiPua1i+ivleivvuaXtuWMhTwvdGQ+PC90cj48dHI+PHRkIGNsYXNzPSJjImFsaWduPSJyaWdodCI+5raI6ICX6K++5YyFMe+8mjwvdGQ+PHRkIGFsaWduPSJsZWZ0Ij7mtYvor5Xor77ml7bljIU8L3RkPjwvdHI+PHRyPjx0ZCBjbGFzcz0iYyJhbGlnbj0icmlnaHQiPua2iOiAl+ivvuWMhTHvvJo8L3RkPjx0ZCBhbGlnbj0ibGVmdCI+5rWL6K+V6K++5pe25YyFPC90ZD48L3RyPjx0cj48dGQgY2xhc3M9ImMiYWxpZ249InJpZ2h0Ij7mtojogJfor77ljIUx77yaPC90ZD48dGQgYWxpZ249ImxlZnQiPua1i+ivleivvuaXtuWMhTwvdGQ+PC90cj48dHI+PHRkIGNsYXNzPSJjImFsaWduPSJyaWdodCI+5raI6ICX6K++5YyFMe+8mjwvdGQ+PHRkIGFsaWduPSJsZWZ0Ij7mtYvor5Xor77ml7bljIU8L3RkPjwvdHI+PHRyPjx0ZCBjbGFzcz0iYyJhbGlnbj0icmlnaHQiPua2iOiAl+ivvuWMhTLvvJo8L3RkPjx0ZCBhbGlnbj0ibGVmdCI+5rWL6K+V6K++5pe25YyFPC90ZD48L3RyPjx0cj48dGQgY2xhc3M9ImMiYWxpZ249InJpZ2h0Ij7liankvZnor77ml7bvvJo8L3RkPjx0ZCBhbGlnbj0ibGVmdCI+NDDor77ml7Y8L3RkPjwvdHI+PC90YWJsZT48ZGl2IGNsYXNzPSJociJzdHlsZT0ibWFyZ2luLXRvcDogMjBweDsiPjxiIHN0eWxlPSJmb250LXNpemU6IDIycHQiPi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLTwvYj48L2Rpdj48ZGl2IGFsaWduPSJjZW50ZXIic3R5bGU9Im1hcmdpbi1ib3R0b206IDNweDsiPuaEn+iwouaCqOeahOWIsOadpe+8gTwvZGl2PjxkaXYgYWxpZ249ImNlbnRlciI+5pyN5Yqh54Ot57q/77yaMDEwLTI4NzIyMzMzPC9kaXY+PC9kaXY+PC9kaXY+PC9ib2R5PjwvaHRtbD4='
    print(html)
    print("----------------------------------------------")
    html = base64.b64decode(html).decode("utf-8")
    print(html)
    # p = Printer.removeHead(urllib.parse.unquote(argvStr))  # 打印机名称
    # p = 'Microsoft Print to PDF'
    p = 'GP-5830 Series'
    app = QApplication(sys.argv)
    ##########################################
    if isJingmo == 1:
        browser = QWebEngineView()
        browser.setWindowTitle('使用PyQt5打印热敏小票')
        browser.resize(1200, 600)
        channel = QWebChannel()
        printer = Print(p)
        channel.registerObject('printer', printer)
        browser.page().setWebChannel(channel)
        url_string = "http://127.0.0.1:8848/demo/test.html"  # 内置的网页地址
        browser.load(QUrl(url_string))
        browser.show()
    else:
        printer = Printer.getPrinter(p)
        Printer.printing(printer, html)

    #####################################################
    sys.exit(app.exec_())
