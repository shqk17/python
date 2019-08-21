from hashlib import sha1
import sys
from PyQt5 import QtWidgets

from work.ryb_pwd_sign import Ui_MainWindow


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("ryb密码生成器")
        self.pushButton.clicked.connect(self.sign_pwd)

    def sign_pwd(self):
        self.lineEdit_4.clear()
        try:
            # 需要加密的字符串
            userId = self.lineEdit.text()
            time_str = self.lineEdit_2.text()+'.0'
            password = self.lineEdit_3.text()
            pwd = userId + password + time_str
            print(pwd)
            # 创建sha1对象
            s1 = sha1()
            # 对s1进行更新
            s1.update(pwd.encode())
            # 加密处理
            result = s1.hexdigest()
            print(result)
            self.lineEdit_4.insert(result)
        except Exception as e:
            print(e)
            self.lineEdit_4.insert(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
