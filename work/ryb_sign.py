import sys, time, hashlib
from PyQt5 import QtWidgets

from work.rybsign_form import Ui_MainWindow


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("ryb签名")
        self.pushButton.clicked.connect(self.OnLoginBtnClicked)

    def OnLoginBtnClicked(self):
        self.textEdit_2.clear()
        urlstr = self.lineEdit.text()
        random = self.lineEdit_2.text()
        params = self.textEdit.toPlainText()
        timestamp =self.timestemp_text.text()
        try:
            random, signStr, str1, timestamp, unSignStr = self.method_sign(params, random, timestamp, urlstr)
            params = params + "&gatewaySign="+ signStr
            random, signStr, str1, timestamp, unSignStr = self.method_sign(params, random, timestamp, urlstr)
            print(signStr)
            url = urlstr + '?' + str1 + '&sign=' + signStr + '&timestamp=' + timestamp + '&randomStr=' + random
            resulturl = 'unSignStr:' + unSignStr + '\n' + '签名字符串：' + signStr + '\n链接地址：\n' + url
            self.textEdit_2.insertPlainText(resulturl)
        except Exception as e:
            print(e)

    def method_sign(self, params, random, timestamp, urlstr):
        if len(urlstr) == 0:
            self.textEdit_2.insertPlainText("请输入需要加密的参数")
        Param = str(params).rstrip().split("&")
        if len(Param) == 0:
            self.textEdit_2.insertPlainText("参数格式不正确")
        Param.sort()
        str1 = "&".join(Param)
        if len(timestamp) == 0:
            timestamp = str(int(time.time()))
        if len(random) == 0:
            random = "qwertyuio"
        str2 = 'timestamp=' + timestamp + '&' + str1 + '&randomStr=' + random
        unSignStr = timestamp + str2.lower()[::-1] + random
        print('unSignStr:' + unSignStr)
        res = hashlib.md5()
        res.update(unSignStr.encode())
        signStr = res.hexdigest()
        return random, signStr, str1, timestamp, unSignStr


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
