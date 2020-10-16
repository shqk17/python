import sys, requests, json
import pymysql
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(516, 681)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 141, 16))
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(160, 10, 321, 31))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 111, 16))
        self.label_2.setObjectName("label_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(160, 50, 321, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(160, 100, 191, 23))
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 150, 111, 16))
        self.label_3.setObjectName("label_3")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(160, 130, 321, 41))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 200, 141, 16))
        self.label_4.setObjectName("label_4")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(160, 190, 321, 41))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 250, 131, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 250, 151, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 310, 451, 291))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 516, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "请输入PROC_INST_ID_："))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "请输入当前任务的主id"))
        self.label_2.setText(_translate("MainWindow", "或者输入task_id_："))
        self.textEdit_2.setPlaceholderText(_translate("MainWindow", "请输入任务id"))
        self.pushButton.setText(_translate("MainWindow", "查询下一个任务节点"))
        self.label_3.setText(_translate("MainWindow", "将跳转到的审批人："))
        self.plainTextEdit.setPlaceholderText(_translate("MainWindow", "可以直接手动输入"))
        self.label_4.setText(_translate("MainWindow", "将跳转到的审批节点名："))
        self.plainTextEdit_2.setPlaceholderText(_translate("MainWindow", "可以直接手动输入"))
        self.pushButton_2.setText(_translate("MainWindow", "直接跳转"))
        self.pushButton_3.setText(_translate("MainWindow", "生成跳转sql"))


class bsUtil():
    def getDBLink(type):
        if type == 1:
            db = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 passwd='123456',
                                 db='ums',
                                 charset='utf8'
                                 , cursorclass=pymysql.cursors.DictCursor
                                 )

        if type == 2:
            db = pymysql.connect(host='rm-8vb1jf512aju12u07fo.mysql.zhangbei.rds.aliyuncs.com',
                                 port=3306,
                                 user='user_ums',
                                 passwd='rJ9dSrO6AMlen1L%#C17@NbD22VGpnt',
                                 db='ums',
                                 charset='utf8'
                                 , cursorclass=pymysql.cursors.DictCursor
                                 )
        if type == 3:
            db = pymysql.connect(host='10.51.4.10',
                                 port=30999,
                                 user='root',
                                 passwd='C5BIi0lJiW',
                                 db='ums',
                                 charset='utf8'
                                 , cursorclass=pymysql.cursors.DictCursor
                                 )

        return db.cursor(), db


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("UMS-审批流跳转工具")
        self.pushButton.clicked.connect(self.queryNext)  # 查询下一个任务节点
        self.pushButton_2.clicked.connect(self.turnIndb)  # 直接跳转
        self.pushButton_3.clicked.connect(self.turnTosql)  # 生成跳转sql

    def turnIndb(self):
        self.turnTosql(1)

    def turnTosql(self, num):
        self.textBrowser.clear()
        self.cursor, self.db = bsUtil.getDBLink(2)
        if self.textEdit.toPlainText() == '' and self.textEdit_2.toPlainText() == '':
            self.textBrowser.append("请输入TASK_ID_或者PROC_INST_ID_！！！！！")
            return

        if self.plainTextEdit.toPlainText() == '' or self.plainTextEdit_2.toPlainText() == '':
            self.textBrowser.append("请输入审批人id或者审批节点名！！！！！")
            return
        activi_task_id = self.textEdit_2.toPlainText()
        activi_PROC_INST_ID_ = self.textEdit.toPlainText()
        activi_usertask = self.plainTextEdit.toPlainText()
        activi_name = self.plainTextEdit_2.toPlainText()
        if self.textEdit.toPlainText() != '' and self.textEdit_2.toPlainText() == '':
            activi_task_id = self.GET_TASKID_BY_PICId(self.textEdit.toPlainText())
            self.textEdit_2.setPlainText(activi_task_id)

        if self.textEdit.toPlainText() == '' and self.textEdit_2.toPlainText() != '':
            activi_PROC_INST_ID_ = self.GET_PICID_BY_TASKID(self.textEdit_2.toPlainText())
            self.textEdit.setPlainText(activi_PROC_INST_ID_)

        sql1 = "update `ums`.`act_ru_task` SET NAME_='%s' ,TASK_DEF_KEY_='%s' where PROC_INST_ID_ ='%s';" % (
            activi_name, activi_usertask, activi_PROC_INST_ID_)
        sql2 = "update `ums`.`act_hi_actinst` SET ACT_ID_='%s' , " \
               " ACT_NAME_='%s'  where PROC_INST_ID_ ='%s'  " \
               "and TASK_ID_='%s' ;" % (activi_usertask, activi_name, activi_PROC_INST_ID_, activi_task_id)
        sql3 = "update `ums`.`act_hi_taskinst` SET NAME_='%s' ," \
               " TASK_DEF_KEY_ ='%s' where PROC_INST_ID_ ='%s'" \
               "  and  END_TIME_ is null;" % (activi_name, activi_usertask, activi_PROC_INST_ID_)
        sql4 = "UPDATE `ums`.`act_ru_execution` SET ACT_ID_='%s' " \
               "WHERE  `PROC_INST_ID_` = '%s'  and BUSINESS_KEY_ is null;" % (activi_usertask, activi_PROC_INST_ID_)
        sql5 = "UPDATE act_ru_identitylink SET GROUP_ID_='%s' WHERE TASK_ID_='%s';" % (activi_name, activi_task_id)
        sql_list = [sql1, sql2, sql3, sql4, sql5]
        for sql in sql_list:
            self.textBrowser.append(sql)
        if len(sql_list) < 5:
            self.textBrowser.append("当前更新sql只有%d条，不满足期望5条，请联系小程序制作者检查" % len(sql_list))
            self.cursor.close()
            self.db.close()
            return
        if num == 1:
            # 执行插入操作
            for sql in sql_list:
                self.cursor.execute(sql)
                self.db.commit()
            # 清空所有的输入框
            self.textEdit.clear()
            self.textEdit_2.clear()
            self.plainTextEdit.clear()
            self.plainTextEdit_2.clear()

        sql_list.clear()
        self.cursor.close()
        self.db.close()

    def GET_PICID_BY_TASKID(self, taskId):
        force_int_sql = "SELECT PROC_INST_ID_ from act_ru_task where ID_='%s'"
        self.cursor.execute(force_int_sql % (taskId))
        result = self.cursor.fetchall()
        if len(result) < 1:
            self.textBrowser.append("错误的TASK_ID_！！！！！")
            return ""
        else:
            return result[0]["PROC_INST_ID_"]

    def GET_TASKID_BY_PICId(self, PICID):
        activi_task_id_sql = "SELECT ID_ from act_ru_task where PROC_INST_ID_='%s';"
        self.cursor.execute(activi_task_id_sql % (PICID))
        result = self.cursor.fetchall()
        if len(result) < 1:
            self.textBrowser.append("错误的PROC_INST_ID_！！！！！")
            return ""
        return result[0]["ID_"]

    def queryNext(self):
        self.textBrowser.clear()
        self.plainTextEdit.clear()
        self.plainTextEdit_2.clear()
        if self.textEdit.toPlainText() == '' and self.textEdit_2.toPlainText() == '':
            self.textBrowser.append("请输入TASK_ID_或者PROC_INST_ID_！！！！！")
            return
            # 开始查询下一个任务节点
        activi_name = ""
        activi_ACT_ID_ = ""
        activi_task_id = ""
        activi_PROC_INST_ID_ = ""
        self.cursor, self.db = bsUtil.getDBLink(2)
        if self.textEdit.toPlainText() != '' and self.textEdit_2.toPlainText() == '':
            self.plainTextEdit.clear()
            self.plainTextEdit_2.clear()
            activi_ACT_ID_sql = "SELECT ACT_ID_ from act_ru_execution where PROC_INST_ID_='%s' and NAME_ IS null;"
            self.cursor.execute(activi_ACT_ID_sql % (self.textEdit.toPlainText()))
            result1 = self.cursor.fetchall()
            if len(result1) < 1:
                self.textBrowser.append("错误的PROC_INST_ID_！！！！！")
                return
            activi_ACT_ID_ = result1[0]["ACT_ID_"]
            activi_task_id = self.GET_TASKID_BY_PICId(self.textEdit.toPlainText())
            activi_PROC_INST_ID_ = self.textEdit.toPlainText()
        if self.textEdit.toPlainText() == '' and self.textEdit_2.toPlainText() != '':
            activi_PROC_INST_ID_ = self.GET_PICID_BY_TASKID(self.textEdit_2.toPlainText())
            activi_task_id = self.textEdit_2.toPlainText()
            activi_ACT_ID_sql = "SELECT ACT_ID_ from act_ru_execution where PROC_INST_ID_='%s' and NAME_ IS null;"
            self.cursor.execute(activi_ACT_ID_sql % (activi_PROC_INST_ID_))
            result1 = self.cursor.fetchall()
            if len(result1) < 1:
                self.textBrowser.append("错误的PROC_INST_ID_！！！！！")
                return
            activi_ACT_ID_ = result1[0]["ACT_ID_"]
        if self.textEdit.toPlainText() != '' and self.textEdit_2.toPlainText() != '':
            activi_task_id = self.textEdit_2.toPlainText()
            activi_PROC_INST_ID_ = self.textEdit.toPlainText()
            activi_ACT_ID_sql = "SELECT ACT_ID_ from act_ru_execution where PROC_INST_ID_='%s' and NAME_ IS null;"
            self.cursor.execute(activi_ACT_ID_sql % (activi_PROC_INST_ID_))
            result1 = self.cursor.fetchall()
            if len(result1) < 1:
                self.textBrowser.append("错误的PROC_INST_ID_！！！！！")
                return
            activi_ACT_ID_ = result1[0]["ACT_ID_"]
        # 到这里获取到了当前执行人是谁，比如usertask38
        url = "http://ums.rybbaby.com/service/history/historic-process-instances/%s?loginAdminUserId=2c948a85701b86cd01702f255e220000&_=1596693085927"
        activi_yewu_name_json = requests.get(url=(url % activi_PROC_INST_ID_))
        name_dict = dict(json.loads(activi_yewu_name_json.content))
        activi_name = name_dict.get("name")
        processDefinitionId = name_dict.get("processDefinitionId")

        activi_url = "http://ums.rybbaby.com/service/repository/process-definitions/%s/model?loginAdminUserId=2c948a85701b86cd01702f255e220000&_=1596693085928"
        activi_shunxu = requests.get(url=(activi_url % processDefinitionId))
        activi_shunxu_dict = dict(json.loads(activi_shunxu.content))
        flowElementMap = dict(dict(activi_shunxu_dict.get("processes")[0]).get("flowElementMap"))
        targetRef_gateway = dict(dict(flowElementMap.get(activi_ACT_ID_)).get("outgoingFlows")[0]).get("targetRef")
        next_userId = ""
        next_name = ""
        for i in dict(flowElementMap.get(targetRef_gateway)).get("outgoingFlows"):
            targetName = str(dict(i).get("targetRef"))
            if targetName.__contains__("user"):
                next_name = dict(flowElementMap.get(targetName)).get("name")
                next_userId = targetName
                break
        if next_userId == "" or next_name == "":
            self.textBrowser.append("未查询到下一个节点！！！！！")
        else:
            self.plainTextEdit.setPlainText(next_userId)
            self.plainTextEdit_2.setPlainText(next_name)
        self.cursor.close()
        self.db.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
