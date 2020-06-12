from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtPrintSupport import QPrinter

#
# 将要打印的东西生成pdf
#
# 908204694@qq.com

a = QApplication([])
document = QTextDocument()
html = """
<head>
<title>Report</title>
<style>
</style>
</head>
<body>
<table width="100%">
<tr>
<td><img src="{}" width="30"></td>
<td><h1>REPORT汉字试试哈</h1></td>
</tr>
</table>
<hr>
<p align=right><img src="{}" width="300"></p>
<p align=right>Sample</p>
</body>
""".format('./aa.png', './bb.png')

document.setHtml(html)
printer = QPrinter()
printer.setResolution(96)
printer.setPageSize(QPrinter.Letter)
printer.setOutputFormat(QPrinter.PdfFormat)
printer.setOutputFileName("test.pdf")

# 设置纸张的边距
printer.setPageMargins(12, 16, 12, 20, QPrinter.Millimeter)
document.setPageSize(QSizeF(printer.pageRect().size()))
print(document.pageSize(), printer.resolution(), printer.pageRect())
document.print_(printer)