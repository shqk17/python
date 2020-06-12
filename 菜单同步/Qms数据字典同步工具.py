import sys
import time
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread

from 菜单同步 import bsUtil
from 菜单同步.数据字典同步 import Ui_MainWindow


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("QMS数据字典同步工具")
        self.saveCaidan.clicked.connect(self.pushSaveCaidan)
        self.thread = None
        self.fromCour = None
        self.fromDb = None
        self.toCour = None
        self.toDb = None

    def pushSaveCaidan(self):
        try:
            # 获取链接
            self.thread = QThreadTask(self.getLink)
            self.thread.signal.connect(self.callback)
            self.thread.start()
        except Exception as e:
            print(e)
            self.textBrowser.insertPlainText("error:\n" + str(e))
            if self.fromDb is not None:
                self.fromDb.close
            if self.toDb is not None:
                self.toDb.close

    def pushSaveAnniu(self):
        try:
            self.getLink(self)
            self.getDeffMenu()
        except Exception as e:
            print(e)
            self.textBrowser.insertPlainText("error")

    def buttonClick(self):
        self.thread = QThreadTask()
        self.thread.signal.connect(self.callback)
        self.thread.start()  # 启动线程

    def getDefDict(self, signal):
        try:
            sql = "select name from sys_dictionary_group"
            signal.emit("···开始对比所有数据字典组···")

            self.fromCour.execute(sql)
            from_result = self.fromCour.fetchall()
            self.toCour.execute(sql)
            to_result = self.toCour.fetchall()
            if len(to_result) < 1 or len(from_result) < 1:
                print("没有数据")
                signal.emit("···未查询到数据集合···")
                return
            else:
                tb_to = []
                for b in to_result:
                    tb_to.append(b["name"])

                tb_to_not = []
                zd_not_in_to = []
                for i in from_result:
                    if tb_to.__contains__(i["name"]):
                        signal.emit("···开始检查<" + str(i["name"]) + ">下数据项是否新增···")
                        # 查询当前 分组下 的相值是否缺少
                        sql1 = "select id from sys_dictionary_group where name ='" + i["name"] + "' "
                        self.toCour.execute(sql1)
                        contents_to_zdian_id = self.toCour.fetchall()
                        self.fromCour.execute(sql1)
                        contents_from_zdian_id = self.fromCour.fetchall()

                        sql2 = "select id,value from sys_dictionary where groupId ='%s'"
                        self.toCour.execute(sql2 % contents_to_zdian_id[0]["id"])
                        contents_to_zdian = self.toCour.fetchall()
                        self.fromCour.execute(sql2 % contents_from_zdian_id[0]["id"])
                        contents_from_zdian = self.fromCour.fetchall()
                        if len(contents_to_zdian) != len(contents_from_zdian):
                            zd_to = []
                            for b in contents_to_zdian:
                                zd_to.append(b["value"])

                            for j in contents_from_zdian:
                                if zd_to.__contains__(j["value"]):
                                    pass
                                else:
                                    signal.emit("···<" + str(i["name"]) + ">下有新增数据项--[" + str(j["value"]) + "]···")
                                    d = {i["name"]: j}
                                    zd_not_in_to.append(d)
                    else:
                        tb_to_not.append(i["name"])
                        signal.emit("···发现新增数据字典组<" + str(i["name"]) + ">···")

                print("新的字典分组：")
                now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
                getGroupData = "select * from sys_dictionary_group where name = '%s' "
                zd_txt = open("./字典变更sql_" + now_time + ".txt", "a")
                signal.emit("···开始生成同步字典组···")
                zd_txt.write("-- 开始同步字典组*****************************\n")
                valueOfGroup = "select * from sys_dictionary where groupId = '%s' "
                for k in tb_to_not:
                    self.fromCour.execute(getGroupData % k)
                    data = self.fromCour.fetchall()[0]
                    signal.emit("···<" + str(data["name"]) + "> 数据同步中···")
                    inset_sql = bsUtil.productSql(data, "sys_dictionary_group")
                    signal.emit("···" + str(inset_sql) + "···")
                    zd_txt.write(str(inset_sql) + "\n")
                    # 查询当前组下所有的字典项
                    self.fromCour.execute(valueOfGroup % data["id"])
                    underGroupData = self.fromCour.fetchall()
                    for ss in underGroupData:
                        under_sql = bsUtil.productSql(ss, "sys_dictionary")
                        signal.emit("···发现字典项" + str(ss["value"]) + " 数据生成中···")
                        signal.emit("···" + str(under_sql) + "···")
                        zd_txt.write(str(under_sql) + "\n")

                signal.emit("···开始同步新增字典项···")
                getZdData = "select * from sys_dictionary where id = '%s' "
                zd_txt.write("-- 开始同步新增字典项*****************************" + "\n")
                for k in zd_not_in_to:
                    self.fromCour.execute(getZdData % list(k.values())[0]["id"])
                    data1 = self.fromCour.fetchall()[0]
                    signal.emit("···发现新增字典项<" + str(data1["value"]) + ">···")
                    inset_sql1 = bsUtil.productSql(data1, "sys_dictionary")
                    signal.emit("···" + str(inset_sql1) + "···")
                    zd_txt.write(str(inset_sql1) + "\n")

                zd_txt.close()
                signal.emit("*********执行完毕*********")

        except Exception as e:
            print(str(e))
            error = open("./error_log.txt", "a")
            error.write(str(e))
            error.close()
            self.textBrowser.insertPlainText("error:\n" + str(e))
            if self.fromDb is not None:
                self.fromDb.close
            if self.toDb is not None:
                self.toDb.close

    def callback(self, msg):
        self.textBrowser.insertPlainText(msg + '[' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ']\n\n')
        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)

    def getLink(self, signal):
        try:
            from_type = self.bg1.checkedId()
            to_type = self.bg2.checkedId()
            signal.emit("···查询数据中请耐心等待···")
            if from_type == 11:
                signal.emit("···选择了测试源···")
                self.fromCour, self.fromDb = bsUtil.getDBLink(1)
            elif from_type == 21:
                signal.emit("···选择了预上线源···")
                self.fromCour, self.fromDb = bsUtil.getDBLink(3)
            elif from_type == 31:
                signal.emit("···选择了正式源···")
                self.fromCour, self.fromDb = bsUtil.getDBLink(2)
            if to_type == 11:
                signal.emit("···选择了测试目标库···")
                self.toCour, self.toDb = bsUtil.getDBLink(1)
            elif to_type == 21:
                signal.emit("···选择了预上线目标库···")
                self.toCour, self.toDb = bsUtil.getDBLink(3)
            elif to_type == 31:
                signal.emit("···选择了正式目标库···")
                self.toCour, self.toDb = bsUtil.getDBLink(2)
            # 去查询数据字典了
            self.getDefDict(signal)
        except Exception as e:
            print(e)
            self.textBrowser.insertPlainText("error" + str(e))
            if self.fromDb is not None:
                self.fromDb.close
            if self.toDb is not None:
                self.toDb.close


class QThreadTask(QThread):
    signal = pyqtSignal(str)  # 括号里填写信号传递的参数

    def __init__(self, func):
        super(QThreadTask, self).__init__()
        self.func = func
        self.result = "none"

    def __del__(self):
        self.wait()

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

    def run(self):
        self.result = self.func(self.signal)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
