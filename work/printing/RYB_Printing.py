# -*- coding: utf-8 -*-
import datetime
import re
import urllib.parse

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinterInfo, QPrinter


class Printer:

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

    @staticmethod
    def getPrinter(p):
        printer = []
        printerInfo = QPrinterInfo()
        print('availablePrinterNames', printerInfo.availablePrinterNames())
        print('defaultPrinterName', printerInfo.defaultPrinterName())
        for item in printerInfo.availablePrinters():
            printer.append(item.printerName())
            log.write(Printer.getTime() + "--availablePrinterName --" + str(item.printerName()))
        if p in printer:
            print(p)
            return p
        else:
            print(printerInfo.defaultPrinterName())
            log.write(Printer.getTime() + "--defaultPrinterName --" + str(printerInfo.defaultPrinterName()))
            return printerInfo.defaultPrinterName()

    @staticmethod
    def printing(printer, context, log):
        print("selected_printer：" + str(printer))
        printerInfo = QPrinterInfo()
        p = QPrinter()
        for item in printerInfo.availablePrinters():
            if printer == str(item.printerName()):
                p = QPrinter(item)

        try:
            doc = QTextDocument()
            doc.setDocumentMargin(0)
            log.write(Printer.getTime() + "--physicalDpiX --" + str(p.physicalDpiX()) + "\n")
            print('physicalDpiX:' + str(p.physicalDpiX()))
            print('resolution:' + str(p.resolution()))
            log.write(Printer.getTime() + "--resolution --" + str(p.resolution()) + "\n")
            print('height:' + str(p.height()))
            log.write(Printer.getTime() + "--height --" + str(p.height()) + "\n")
            print('width:' + str(p.width()))
            log.write(Printer.getTime() + "--width --" + str(p.width()) + "\n")
            scale = round(p.physicalDpiX() / p.resolution(), 4)
            print('scale:' + str(scale))
            log.write(Printer.getTime() + "--scale --" + str(scale) + "\n")
            print('supportedResolutions:' + str(p.supportedResolutions()))
            log.write(Printer.getTime() + "--supportedResolutions --" + str(p.supportedResolutions()) + "\n")
            print('logicalDpiX:' + str(p.logicalDpiX()))
            log.write(Printer.getTime() + "--logicalDpiX --" + str(p.logicalDpiX()) + "\n")
            doc.setPageSize(
                QSizeF(p.logicalDpiX() * (p.width() / 25.4 / scale),
                       p.logicalDpiY() * (p.height() / 25.4 / scale)))
            doc.setHtml(context)
            print("starting print")
            p.setOutputFormat(QPrinter.NativeFormat)
            doc.print_(p)
        except Exception as ee:
            print(ee)
            log.write(Printer.getTime() + "***print - error****" + str(ee) + "\n")
            log.close()


if __name__ == '__main__':
    # -*- coding: utf-8 -*-
    import sys, base64
    from PyQt5.QtWidgets import QApplication

    print(str(sys.argv[0]))
    log = open(
        str(sys.argv[0]).rsplit("\\", 1)[0] + "\RYBPRINTING" + datetime.datetime.now().strftime('%Y-%m') + ".log", "a")
    try:
        # 1.打印机(为空，使用默认打印机) 2.html
        argvStr = str(sys.argv[1]).split(",")[0]
        log.write(Printer.getTime() + "-- argvStr --" + argvStr + "\n")
        print(argvStr)
        html = str(sys.argv[1]).split(",")[1]
        log.write(Printer.getTime() + "-- html --" + html + "\n")
        # html = 'PGh0bWw+PHN0eWxlPiNteXNvY2tldFByaW50e2ZvbnQtZmFtaWx5Oiflvq7ova/pm4Xpu5EnLCdNaWNyb3NvZnQgWWFIZWknO2ZvbnQtc2l6ZToxNXB0fS5wcmludC1ib3h7d2lkdGg6MTAwJTttYXJnaW4tdG9wOjIwcHg7bGluZS1oZWlnaHQ6MTJwdH10ZHtmb250LXNpemU6MTVwdH0uY3twYWRkaW5nLWxlZnQ6MjBweH08L3N0eWxlPjxib2R5PjxkaXYgd2lkdGg9IjMwMHB4ImlkPSJteXNvY2tldFByaW50Ij48ZGl2IGNsYXNzPSJwcmludC1ib3giPjxkaXYgYWxpZ249ImNlbnRlciJzdHlsZT0iZm9udC1zaXplOiAyMnB0Owlmb250LXdlaWdodDogNTAwOyI+57qi6buE6JOd5Lqy5a2Q5ZutPC9kaXY+PGRpdiBjbGFzcz0iaHIiPjxiIHN0eWxlPSJmb250LXNpemU6IDIycHQ7Ij4tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS08L2I+PC9kaXY+PGRpdiBhbGlnbj0iY2VudGVyInN0eWxlPSJtYXJnaW4tYm90dG9tOiAzcHg7Ij4yMDE55bm0MTHmnIgyNuaXpTA5OjU0PC9kaXY+PGRpdiBhbGlnbj0iY2VudGVyIj7nrb7liLDlrp3lrp3vvJrjgJDkuo7kvbPkuZDjgJE8L2Rpdj48ZGl2IGNsYXNzPSJociJzdHlsZT0ibWFyZ2luLXRvcDogMjBweDsiPjxiIHN0eWxlPSJmb250LXNpemU6IDIycHQiPi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLTwvYj48L2Rpdj48dGFibGU+PHRyPjx0ZCBjbGFzcz0iYyJhbGlnbj0icmlnaHQiPuivvueoi+WQjeensO+8mjwvdGQ+PHRkIGFsaWduPSJsZWZ0Ij7pn7PkuZBJSTwvdGQ+PC90cj48dHI+PHRkIGNsYXNzPSJjImFsaWduPSJyaWdodCI+5LiK6K++5pe26Ze077yaPC90ZD48dGQgYWxpZ249ImxlZnQiPjExOjUzOjQ1PC90ZD48L3RyPjx0cj48dGQgY2xhc3M9ImMiYWxpZ249InJpZ2h0Ij7mjojor77ogIHluIjvvJo8L3RkPjx0ZCBhbGlnbj0ibGVmdCI+6ICB5biI5LiAZmdmZ2dnPC90ZD48L3RyPjx0cj48dGQgY2xhc3M9ImMiYWxpZ249InJpZ2h0Ij7mtojogJfor77ml7bvvJo8L3RkPjx0ZCBhbGlnbj0ibGVmdCI+MeivvuaXtjwvdGQ+PC90cj48dHI+PHRkIGNsYXNzPSJjImFsaWduPSJyaWdodCI+5raI6ICX6K++5YyF77yaPC90ZD48dGQgYWxpZ249ImxlZnQiPua1i+ivleivvuaXtuWMhTwvdGQ+PC90cj48dHI+PHRkIGNsYXNzPSJjImFsaWduPSJyaWdodCI+5raI6ICX6K++5YyFMe+8mjwvdGQ+PHRkIGFsaWduPSJsZWZ0Ij7mtYvor5Xor77ml7bljIU8L3RkPjwvdHI+PHRyPjx0ZCBjbGFzcz0iYyJhbGlnbj0icmlnaHQiPua2iOiAl+ivvuWMhTHvvJo8L3RkPjx0ZCBhbGlnbj0ibGVmdCI+5rWL6K+V6K++5pe25YyFPC90ZD48L3RyPjx0cj48dGQgY2xhc3M9ImMiYWxpZ249InJpZ2h0Ij7mtojogJfor77ljIUx77yaPC90ZD48dGQgYWxpZ249ImxlZnQiPua1i+ivleivvuaXtuWMhTwvdGQ+PC90cj48dHI+PHRkIGNsYXNzPSJjImFsaWduPSJyaWdodCI+5raI6ICX6K++5YyFMe+8mjwvdGQ+PHRkIGFsaWduPSJsZWZ0Ij7mtYvor5Xor77ml7bljIU8L3RkPjwvdHI+PHRyPjx0ZCBjbGFzcz0iYyJhbGlnbj0icmlnaHQiPua2iOiAl+ivvuWMhTLvvJo8L3RkPjx0ZCBhbGlnbj0ibGVmdCI+5rWL6K+V6K++5pe25YyFPC90ZD48L3RyPjx0cj48dGQgY2xhc3M9ImMiYWxpZ249InJpZ2h0Ij7liankvZnor77ml7bvvJo8L3RkPjx0ZCBhbGlnbj0ibGVmdCI+NDDor77ml7Y8L3RkPjwvdHI+PC90YWJsZT48ZGl2IGNsYXNzPSJociJzdHlsZT0ibWFyZ2luLXRvcDogMjBweDsiPjxiIHN0eWxlPSJmb250LXNpemU6IDIycHQiPi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLTwvYj48L2Rpdj48ZGl2IGFsaWduPSJjZW50ZXIic3R5bGU9Im1hcmdpbi1ib3R0b206IDNweDsiPuaEn+iwouaCqOeahOWIsOadpe+8gTwvZGl2PjxkaXYgYWxpZ249ImNlbnRlciI+5pyN5Yqh54Ot57q/77yaMDEwLTI4NzIyMzMzPC9kaXY+PC9kaXY+PC9kaXY+PC9ib2R5PjwvaHRtbD4='
        print(html)
        print("----------------------------------------------")
        html = base64.b64decode(html).decode("utf-8")
        log.write(Printer.getTime() + "--after decode html --" + html + "\n")
        p = base64.b64decode(urllib.parse.unquote(Printer.removeHead(argvStr))).decode("utf-8")  # 打印机名称
        log.write(Printer.getTime() + "--printer --" + p + "\n")
        # p = 'Microsoft Print to PDF'
        # p = 'GP-5830 Series'
        app = QApplication(sys.argv)
        ##########################################
        printer = Printer.getPrinter(p)
        Printer.printing(printer, html, log)
    except Exception as e:
        print(e)
        log.write(Printer.getTime() + "***error****" + str(e) + "\n")
        log.close()

    #####################################################
    log.close()
    sys.exit(app.exec_())
