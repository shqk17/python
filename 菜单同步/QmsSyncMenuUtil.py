# coding:utf-8
# -*- coding: utf-8 -*-
import sys
import time
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5 import sip
from 菜单同步 import bsUtil
from 菜单同步.MenuButton import Ui_MainWindow


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("UMS菜单按钮同步")
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
            self.textBrowser.insertPlainText("error")
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

    def getDeffMenu(self, caidanName, signal):
        try:

            caidanStr = "一级菜单"
            allCaidanSql = "SELECT * FROM sys_menu_permissions where pId is null"
            if caidanName is None or caidanName == '':
                signal.emit("···开始对比所有菜单权限···")
            else:
                signal.emit("···开始对比指定菜单《" + caidanName + "》权限···")
                caidanStr = caidanName + " 菜单"
                allCaidanSql = "SELECT * FROM sys_menu_permissions where `name` IN ('" + caidanName + "');"
            from_result, diff_list = self.bijiaoCaidan(signal, allCaidanSql, caidanStr)
            signal.emit("···请注意即将生成sql 到同级目录的MenuAiSql.txt文件中···")
            now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            MenuAiSql = open("./MenuAiSql_" + now_time + ".txt", "a")
            MenuAiSql.write("-- QmsSyncMenuUtil AUTO PRODUCT SQL ------\n")

            for menu in from_result:
                if diff_list.__contains__(menu["id"]):
                    MenuAiSql.write("-- 菜单同步sql------\n")
                    MenuAiSql.write("-- Mark正在处理菜单《" + str(menu["name"]) + "》------\n")
                    inset_sql = bsUtil.productSql(menu, "sys_menu_permissions")
                    MenuAiSql.write(str(inset_sql))
                    # 既然是新增的，必然可能有新增按钮，随便把按钮也处理了
                    self.findDiffAnNiu(menu['id'], signal, MenuAiSql)
                if menu["pId"] is None or menu["pId"] == "":
                    self.compareSencondCaidan(menu["id"], signal, MenuAiSql)
                else:
                    self.compareTongJiCaidan(menu["id"], signal, MenuAiSql)

            MenuAiSql.close()
            signal.emit("···同步sql已生成完毕···")
            if self.fromDb is not None:
                self.fromDb.close
            if self.toDb is not None:
                self.toDb.close
        except Exception as e:
            print(str(e))
            error = open("./error_log.txt", "a")
            error.write(str(e))
            error.close()
            self.textBrowser.insertPlainText("error")
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
                signal.emit("···选择了本地源···")
                self.fromCour, self.fromDb = bsUtil.getDBLink(1)
            elif from_type == 21:
                signal.emit("···选择了测试源···")
                self.fromCour, self.fromDb = bsUtil.getDBLink(3)
            elif from_type == 31:
                signal.emit("···选择了正式源···")
                self.fromCour, self.fromDb = bsUtil.getDBLink(2)
            if to_type == 11:
                signal.emit("···选择了本地目标库···")
                self.toCour, self.toDb = bsUtil.getDBLink(1)
            elif to_type == 21:
                signal.emit("···选择了测试目标库···")
                self.toCour, self.toDb = bsUtil.getDBLink(3)
            elif to_type == 31:
                signal.emit("···选择了正式目标库···")
                self.toCour, self.toDb = bsUtil.getDBLink(2)
            # 去查找菜单按钮了
            self.getDeffMenu(self.caidanName.text(), signal)
        except Exception as e:
            print(e)
            self.textBrowser.insertPlainText("error")
            if self.fromDb is not None:
                self.fromDb.close
            if self.toDb is not None:
                self.toDb.close

    def compareTongJiCaidan(self, menuId, signal, MenuAiSql):
        sql = "SELECT * FROM sys_menu_permissions where id ='" + menuId + "' "
        from_result, diff_list = self.bijiaoCaidan(signal, sql, '二级菜单')
        for menu in from_result:
            if diff_list.__contains__(menu["id"]):
                MenuAiSql.write("-- 二级菜单同步sql------\n")
                MenuAiSql.write("-- Mark正在处理菜单《" + str(menu["name"]) + "》------\n")
                inset_sql = bsUtil.productSql(menu, "sys_menu_permissions")
                MenuAiSql.write(str(inset_sql))
            self.findDiffAnNiu(menu['id'], signal, MenuAiSql)

    def compareSencondCaidan(self, menuId, signal, MenuAiSql):
        sql = "SELECT * FROM sys_menu_permissions where pId ='" + menuId + "' "
        from_result, diff_list = self.bijiaoCaidan(signal, sql, '二级菜单')
        for menu in from_result:
            if diff_list.__contains__(menu["id"]):
                MenuAiSql.write("-- 二级菜单同步sql------\n")
                MenuAiSql.write("-- Mark正在处理菜单《" + str(menu["name"]) + "》------\n")
                inset_sql = bsUtil.productSql(menu, "sys_menu_permissions")
                MenuAiSql.write(str(inset_sql))
            self.findDiffAnNiu(menu['id'], signal, MenuAiSql)

    def bijiaoCaidan(self, signal, sql, type):
        self.fromCour.execute(sql)
        from_result = self.fromCour.fetchall()
        self.toCour.execute(sql)
        to_result = self.toCour.fetchall()
        from_queshao, to_queshao = bsUtil.bijiao2(bsUtil.suoyin(from_result), bsUtil.suoyin(to_result))
        diff_list = []
        if from_queshao is None and to_queshao is None:
            pass
        if from_queshao is None and to_queshao is not None:
            signal.emit("···目标库的" + type + "比源库还多？？？···")
        if from_queshao is not None and to_queshao is None:
            for i in from_queshao:
                signal.emit(
                    "···查询到新增的" + type + "---->" + str.split(i, ',')[1] + "(id:" + str.split(i, ',')[
                        0] + ")···")
                diff_list.append(str.split(i, ',')[0])
        return from_result, diff_list

    def findDiffAnNiu(self, menuId, signal, MenuAiSql):
        sql = "SELECT * FROM sys_handle_permissions WHERE menuId ='" + menuId + "' AND rolePermissionAllotId IS NULL AND adminUserPermissionAllotId IS NULL;"
        from_result, diff_list = self.bijiaoCaidan(signal, sql, '按钮')
        for menu in from_result:
            if diff_list.__contains__(menu["id"]):
                signal.emit("···正在执行按钮同步(" + menu["id"] + ")···")
                MenuAiSql.write("-- 按钮同步sql------\n")
                inset_sql = bsUtil.productSql(menu, "sys_handle_permissions")
                MenuAiSql.write(str(inset_sql))
                self.finDiffAttr(menu['id'], signal, MenuAiSql)
                self.finDiffclass(menu['id'], signal, MenuAiSql)
                self.finDiffevents(menu['id'], signal, MenuAiSql)
                self.finDiffstyles(menu['id'], signal, MenuAiSql)

    def finDiffAttr(self, attrId, signal, MenuAiSql):
        sql = "SELECT * FROM sys_handle_permissions_attrs WHERE handlePermissionId ='%s';"
        sql = sql % (attrId)
        from_result, diff_list = self.bijiaoCaidan(signal, sql, '按钮Attr')
        for menu in from_result:
            if diff_list.__contains__(menu["id"]):
                signal.emit("···正在执行按钮--Attr同步(" + menu["id"] + ")···")
                MenuAiSql.write("-- 按钮Attr同步sql------\n")
                inset_sql = bsUtil.productSql(menu, "sys_handle_permissions_attrs")
                MenuAiSql.write(str(inset_sql))

    def finDiffclass(self, classId, signal, MenuAiSql):
        sql = "SELECT * FROM sys_handle_permissions_classes WHERE handlePermissionId ='%s' ;"
        sql = sql % (classId)
        from_result, diff_list = self.bijiaoCaidan(signal, sql, '按钮Class')
        for menu in from_result:
            if diff_list.__contains__(menu["id"]):
                signal.emit("···正在执行按钮--Class同步(" + menu["id"] + ")···")
                MenuAiSql.write("-- 按钮Class同步sql------\n")
                inset_sql = bsUtil.productSql(menu, "sys_handle_permissions_classes")
                MenuAiSql.write(str(inset_sql))

    def finDiffevents(self, eventsId, signal, MenuAiSql):
        sql = "SELECT * FROM sys_handle_permissions_events WHERE handlePermissionId ='%s' ;"
        sql = sql % (eventsId)
        from_result, diff_list = self.bijiaoCaidan(signal, sql, '按钮events')
        for menu in from_result:
            if diff_list.__contains__(menu["id"]):
                signal.emit("···正在执行按钮--events同步(" + menu["id"] + ")···")
                MenuAiSql.write("-- 按钮events同步sql------\n")
                inset_sql = bsUtil.productSql(menu, "sys_handle_permissions_events")
                MenuAiSql.write(str(inset_sql))

    def finDiffstyles(self, stylesId, signal, MenuAiSql):
        sql = "SELECT * FROM sys_handle_permissions_styles WHERE handlePermissionId ='%s' ;"
        sql = sql % (stylesId)
        from_result, diff_list = self.bijiaoCaidan(signal, sql, '按钮styles')
        for menu in from_result:
            if diff_list.__contains__(menu["id"]):
                signal.emit("···正在执行按钮--styles同步(" + menu["id"] + ")···")
                MenuAiSql.write("-- 按钮styles同步sql------\n")
                inset_sql = bsUtil.productSql(menu, "sys_handle_permissions_styles")
                MenuAiSql.write(str(inset_sql))


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
