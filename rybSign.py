import sys, time, hashlib
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import requests
import json
from rybsignv2 import Ui_MainWindow


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("ryb签名")
        self.pushButton.clicked.connect(self.SignUrl)
        self.pushButton_2.clicked.connect(self.RequestInfoBtnClicked)

    def RequestInfoBtnClicked(self):
        try:
            self.textEdit_4.clear()
            isPost = self.radioButton.isChecked()
            urlstr = self.textEdit_3.toPlainText()
            bodystr = self.textEdit_5.toPlainText()
            if len(urlstr) < 1:
                self.textEdit_4.insertPlainText("请输入url链接")
                return
            if len(bodystr) < 1:
                bodystr = None
            url = urlstr
            s = bodystr
            r = ""
            if isPost:
                r = requests.post(url, data=s)
            else:
                r = requests.post(url, data=s)
            if r.status_code == 200:
                self.textEdit_4.insertPlainText(r.text)
            else:
                self.textEdit_4.insertPlainText(r.text)

        except Exception as e:
            self.textEdit_4.insertPlainText(str(e))

    def SignUrl(self):
        try:
            self.textEdit_2.clear()
            self.textEdit_3.clear()
            urlstr = self.lineEdit.text()
            random = self.lineEdit_2.text()
            params = self.textEdit.toPlainText()
            timestamp = self.timestemp_text.text()
            Param = []
            if len(urlstr) == 0:
                self.textEdit_2.insertPlainText("请输入需要加密的参数")
                return
            # 解析带参数的链接
            signParam = ["timestamp", "sign", "randomStr"]
            for sp in signParam:
                if sp in urlstr:
                    Param = urlstr.split("?")[1].split("&")
                    urlstr = urlstr.split("?")[0]
                    for x in reversed(Param):
                        if x.split("=")[0] in signParam:
                            Param.remove(x)
                        else:
                            pass
                    break
                else:
                    Param = str(params).rstrip().split("&")
            if len(Param) == 0:
                self.textEdit_2.insertPlainText("参数格式不正确")
                return
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
            print(signStr)
            url = urlstr + '?' + str1 + '&sign=' + signStr + '&timestamp=' + timestamp + '&randomStr=' + random
            resulturl = 'unSignStr:\n' + unSignStr + '\n' + '签名字符串：' + signStr
            self.textEdit_2.insertPlainText(resulturl)
            self.textEdit_3.insertPlainText(url)
        except Exception as e:
            print(e)
            self.textEdit_3.insertPlainText("error")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
