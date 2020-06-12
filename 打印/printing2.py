# ------------------------- printer.py ----------------------
# 直接打印,不预览

# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtPrintSupport import QPrinterInfo, QPrinter


class Printer:
    # 打印机列表
    @staticmethod
    def printerList():
        printer = []
        printerInfo = QPrinterInfo()
        print('availablePrinterNames', printerInfo.availablePrinterNames())
        print('defaultPrinterName', printerInfo.defaultPrinterName())

        for item in printerInfo.availablePrinters():
            printer.append(item.printerName())
        return printer, printerInfo.defaultPrinterName()

    # 打印任务
    @staticmethod
    def printing(printer, context):
        p = QPrinter()

        doc = QTextDocument()

        htmlStr = context
        print('aaaa', htmlStr)
        doc.setHtml(htmlStr)
        doc.setPageSize(QSizeF(p.logicalDpiX() * (80 / 25.4),
                               p.logicalDpiY() * (297 / 25.4)))
        p.setOutputFormat(QPrinter.NativeFormat)
        doc.print_(p)

    @staticmethod
    def printing_22(printer, context):
        printerInfo = QPrinterInfo()
        p = QPrinter()
        for item in printerInfo.availablePrinters():
            if printer == str(item.printerName()):
                p = QPrinter(item)
                doc = QTextDocument()
                font = doc.defaultFont()
                font.setBold(True)
                font.setPointSize(font.pointSize() + 1)
                doc.setDefaultFont(font)
                font.setPixelSize(5)
                # doc.setPageSize(QSizeF(p.logicalDpiX() * (88 / 25.4),
                #                        p.logicalDpiY() * (297 / 25.4)))
                # x是间距，数字越小间距越大 y是纵长度 越大长度越小
                doc.setPageSize(QSizeF(p.logicalDpiX() * (60 / 25.4), p.logicalDpiY() * (3500 / 25.4)))
                p.setOutputFormat(QPrinter.NativeFormat)
                doc.setHtml(u'%s' % context)
                doc.print_(p)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    argvStr = sys.argv[1]
    print(argvStr)
    csMap = str.split(argvStr, ",")
    data = tuple(csMap)
    # data = ('11', '22', '33', '44', '55', '66', '77', '88', '99')
    app = QApplication(sys.argv)
    ##########################################
    html = '<html> ' \
           '<head></head>' \
           '<style type="text/css">' \
           '	.pd-r {' \
           'padding-right: 60px' \
           ' }' \
           '.c {' \
           '	margin: 0 auto;' \
           '	font-size: 15px;' \
           '	margin-bottom: 5px;' \
           '}' \
           '	.hr {' \
           '		font-family: "宋体";' \
           '		font-size: 5pt;' \
           '		border-bottom: 2px dashed #000;' \
           '		margin: 5px 0;' \
           '		width: 100%;' \
           '	}' \
           '</style>' \
           '<body ><div class="modal-body"><div class="bootbox-body">' \
           '<div class="print-page">' \
           '    <div id="myPrint"><div class="print-box">' \
           '<h4 class="pd-r">红黄蓝亲子园</h4>' \
           '<div class="hr">' \
           '</div><div class="c pd-r">' + data[0] + '</div>' \
                                                    '<div class="c pd-r">签到宝宝：【' + data[1] + '】</div>' \
                                                                                             '<div class="hr"></div><div class="c"><label>' \
                                                                                             '课程名称：</label><span>' + \
           data[2] + '</span>' \
                     '</div><div class="c"><label>上课时间：</label><span>' + data[3] + '</span></div>' \
                                                                                   '<div class="c"><label>上课教室：</label><span>' + \
           data[4] + '</span></div><div class="c">' \
                     '<label>授课老师：</label><span>' + data[5] + '</span></div><div class="c">' \
                                                              '<label>消耗课时：</label><span>' + data[
               6] + '</span></div><div class="c">' \
                    '<label>消耗课包：</label><span>' + data[7] + '</span></div>' \
                                                             '<div class="c"><label>剩余课时：</label><span>' + data[
               8] + '</span>' \
                    '</div><div class="hr"></div>' \
                    '<div class="pd-r" style="margin-bottom: 5px;">感谢您的到来！</div>' \
                    '<div class="pd-r">服务热线：010-28722333</div></div></div>' \
                    '</div>' \
                    '</body>' \
                    '</html>'
    print(html)
    p = "DL-581P(NEW)"  # 打印机名称
    # Printer.printing(p, html)
    printer, defaultPrinter = Printer.printerList()
    print("默认打印机：" + defaultPrinter)
    Printer.printing_22(defaultPrinter, html)

    #####################################################
    sys.exit(app.exec_())
