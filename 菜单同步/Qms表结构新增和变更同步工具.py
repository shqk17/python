import sys
import time, re
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread

from 菜单同步 import bsUtil
from 菜单同步.表结构新增和变更 import Ui_MainWindow


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("UMS表结构新增和变更同步工具")
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
            self.textBrowser.insertPlainText("error:\n"+str(e))
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

    def getDefDict(self,signal):
        try:
            ziduanSql = "select * from %s limit 1"
            sql = " show tables ; "
            signal.emit("···开始对比所有数据表···")
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
                    tb_to.append(b["Tables_in_ums"].lower())

                tb_to_not = []
                zd_not_in_to = {}
                for i in from_result:
                    if tb_to.__contains__(i["Tables_in_ums"].lower()):
                        pattern = re.compile(r'view')
                        if re.findall(pattern, str(i["Tables_in_ums"])):
                            # 证明是视图略过
                            continue

                        print("···开始检查<" + str(i["Tables_in_ums"]) + ">下是否新增字段···")
                        signal.emit("···开始检查<" + str(i["Tables_in_ums"]) + ">下是否新增字段···")
                        self.toCour.execute(ziduanSql % str(i["Tables_in_ums"]))
                        contents_to_zd_id = self.toCour.fetchall()
                        self.fromCour.execute(ziduanSql % str(i["Tables_in_ums"]))
                        contents_from_zd_id = self.fromCour.fetchall()
                        to_col_name_list = [tuple_to[0] for tuple_to in self.toCour.description]
                        from_col_name_list = [tuple_from[0] for tuple_from in self.fromCour.description]
                        if len(to_col_name_list) != len(from_col_name_list):
                            print("发现字段数不同")
                            zd_to = []
                            for b in to_col_name_list:
                                zd_to.append(b.lower())

                            for j in from_col_name_list:
                                if zd_to.__contains__(j.lower()):
                                    pass
                                else:
                                    signal.emit("···<" + str(i["Tables_in_ums"]) + ">下有新增字段--["+str(j)+"]···")
                                    zd_not_in_to[i["Tables_in_ums"]] = j
                    else:
                        tb_to_not.append(i["Tables_in_ums"])
                        signal.emit("···发现新增表<" + str(i["Tables_in_ums"]) + ">···")

                now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
                zd_txt = open("./表结构新增或变更sql_" + now_time + ".txt", "a")
                signal.emit("···开始生成表结构新增或变更同步sql···")
                zd_txt.write("-- 开始同步表结构*****************************\n")

                pass_tb = {"C3P0TestTable"}
                createSql = "show create table %s;"
                pattern = re.compile(r'copy')
                pattern2 = re.compile(r'\d+$')
                for k in tb_to_not:
                    print(str(k))
                    if pass_tb.__contains__(str(k)):
                        continue

                    if re.findall(pattern, str(k)):
                        continue

                    if re.findall(pattern2, str(k)):
                        continue

                    self.fromCour.execute(createSql % k)
                    data = self.fromCour.fetchall()[0]
                    signal.emit("···<"+str(data["Table"])+"> 数据同步中···")
                    zd_txt.write(str(data["Create Table"])+";\n")

                if len(zd_not_in_to) <= 0:
                    signal.emit("···未检测到新增字段···")
                    zd_txt.write("-- 未检测到新增字段*****************************" + "\n")
                    zd_txt.close()
                    signal.emit("*********执行完毕*********")
                else:
                    signal.emit("···开始同步新增字段共"+str(len(zd_not_in_to))+"条···")
                    zd_txt.write("-- 新增字段需手动同步*****************************"+"\n")
                    for k, v in zd_not_in_to.items():
                        signal.emit("···表《"+str(k)+"》发现新增字段<"+str(v)+">···")
                        zd_txt.write("···表《"+str(k)+"》发现新增字段<"+str(v)+">···"+"\n")

                    zd_txt.close()
                    signal.emit("*********执行完毕*********")

        except Exception as e:
            print(str(e))
            error = open("./error_log.txt", "a")
            error.write(str(e))
            error.close()
            self.textBrowser.insertPlainText("error:\n"+str(e))
            if self.fromDb is not None:
                self.fromDb.close
            if self.toDb is not None:
                self.toDb.close


    def callback(self, msg):
        self.textBrowser.insertPlainText(msg + '[' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+']\n\n')
        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)

    def getLink(self, signal):
        try:
            from_type = self.bg1.checkedId()
            to_type = self.bg2.checkedId()
            signal.emit("···查询数据中请耐心等待···")
            if from_type == 11:
                signal.emit("···选择了本地测试源···")
                self.fromCour, self.fromDb = bsUtil.getDBLinkUms(1)
            elif from_type == 21:
                signal.emit("···选择了预上线源···")
                self.fromCour, self.fromDb = bsUtil.getDBLinkUms(3)
            elif from_type == 31:
                signal.emit("···选择了正式源···")
                self.fromCour, self.fromDb = bsUtil.getDBLinkUms(2)
            if to_type == 11:
                signal.emit("···选择了测试目标库···")
                self.toCour, self.toDb = bsUtil.getDBLinkUms(1)
            elif to_type == 21:
                signal.emit("···选择了预上线目标库···")
                self.toCour, self.toDb = bsUtil.getDBLinkUms(3)
            elif to_type == 31:
                signal.emit("···选择了正式目标库···")
                self.toCour, self.toDb = bsUtil.getDBLinkUms(2)
            # 去查询数据字典了
            self.getDefDict(signal)
        except Exception as e:
            print(e)
            self.textBrowser.insertPlainText("error"+str(e))
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
