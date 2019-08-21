import datetime
import re
import sys
from functools import reduce

from PyQt5 import QtWidgets

import bsUtil
from QMS_packagehistory_check_util import Ui_MainWindow


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("QMS")
        self.pushButton.clicked.connect(self.checkPackage)

    def format_time(self, str_time):
        tm = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        time_offset = tm - datetime.timedelta(seconds=-1)
        return time_offset.strftime("%Y-%m-%d %H:%M:%S")

    def checkHaveReturnClass(self, row, memberIdBind):
        updateTime = row["updateTime"]
        memberId = row["memberId"]
        sql = ""
        self.cursor.execute(sql % (memberId))
        result = self.cursor.fetchall()
        pass

    def compareNum(self, first, second):
        if int(first) > int(second):
            return "+"
        elif int(first) == int(second):
            return "="
        else:
            return "-"

    def checkOperate(self, operateStr):
        operateMap = {
            "-+==": "报班",
            "=-+=": "0-1*0-5",  # 考勤 或者 0-5
            "+-==": "0-2",  # 退班
            "=-++": "0-3",
            "=-=+": "0-3",
            "+=-=": "1-2*5-2*考勤退课",  # 1-2或者 考勤退课 或者 5-2
            "==-+": "1-3*1-6*补课取消考勤*5-3",  # 或者 1-6  补课取消考勤 或者5-3
            "===+": "1-6",  # 补课取消考勤
            "-=+=": "2-1*2-5",  # 或者 2-5
            "-==+": "2-3",
            "==+-": "3-1*3-5",  # 或者 3-5
            "+==-": "3-2",
            "+===": "加课时操作",
            "-===": "减课时操作",
            "===-": "减补课操作",
            "==+-": "减补课操作",
            "====": "1-5"  # 无操作或者1-5 5-1
        }
        if operateStr not in operateMap.keys():
            return "未知操作"
        return operateMap[operateStr]

    def compareClassChange(self, lastInfo, row):
        last_one = lastInfo["surplusClassHour"]
        last_two = lastInfo["unusedClassHour"]
        last_three = lastInfo["consumptionClassHour"]
        last_four = lastInfo["remediationClassHour"]
        now_one = row["surplusClassHour"]
        now_two = row["unusedClassHour"]
        now_three = row["consumptionClassHour"]
        now_four = row["remediationClassHour"]
        fuhao_one = self.compareNum(now_one, last_one)
        fuhao_two = self.compareNum(now_two, last_two)
        fuhao_three = self.compareNum(now_three, last_three)
        fuhao_four = self.compareNum(now_four, last_four)
        list = [float(now_one) - float(last_one), \
                float(now_two) - float(last_two), \
                float(now_three) - float(last_three), \
                float(now_four) - float(last_four) \
                ]
        fuhao = fuhao_one + fuhao_two + fuhao_three + fuhao_four
        return self.checkOperate(fuhao), list, fuhao

    @staticmethod
    def checkAttendInfo(row, list):
        sql = "select ROUND(count(id)*formalClass+giftClass+remedialClass) as classHour " \
              "from tss_member_check_attendance_history where memberId ='2c92828665c3349b0165c361747822ad' " \
              "and updateTime='2018-09-19 16:34:00'"
        pass

    def checkKaoQing(self, row, list, memberIdBind):
        after_time = self.format_time(str(row["updateTime"]))
        member_id = row["memberId"]
        sql = "select attendClassId,formalClass,giftClass,remedialClass,updateTime,attendenceStatus  from tss_member_check_attendance_history " \
              "where memberId ='%s' and updateTime = '%s' order by updateTime"
        is_find, attend_id, attendence_status = self.method_checkAttendHistory(after_time, member_id, row, sql)
        return_memebr_id = member_id
        return_message = ""
        if is_find is not True:
            if len(memberIdBind) < 1:
                return_message = "A会员:\t\n" + str(row["updateTime"]) + " 的考勤 信息未找到 "
            else:
                is_bind_find, attend_id, attendence_status = self.method_checkAttendHistory(after_time, memberIdBind,
                                                                                            row, sql)
                return_memebr_id = memberIdBind
                if is_bind_find is not True:
                    return_message = "A,B会员" + ":\t\n" + str(row["updateTime"]) + " 会员的考勤 信息未找到 "

        return attend_id, return_memebr_id, attendence_status, return_message

    def method_checkAttendHistory(self, afterTime, memberId, row, sql):
        self.cursor.execute(sql % (memberId, afterTime))
        result = self.cursor.fetchall()
        if len(result) > 0:
            for i in result:
                print(i)
            return True, result[0]["attendClassId"], result[0]["attendenceStatus"]

        else:
            self.cursor.execute(sql % (memberId, row["updateTime"]))
            result1 = self.cursor.fetchall()
            if len(result1) > 0:
                for j in result1:
                    print(j)
                return True, result1[0]["attendClassId"], result1[0]["attendenceStatus"]
            else:
                return False, None, -1

    def checkPackageHistory(self, data):
        self.resultText.clear()
        # 未知操作
        un_know_oper = []
        # 考勤重复的可能问题
        kaoqing_chongfu_check = []
        # 考勤 操作同课节多次
        alert_kaoqing = []
        # 报班消耗课节数
        attend_num = 0
        sql = "select id,memberId,packageName,surplusClassHour,consumptionClassHour," \
              "unusedClassHour,remediationClassHour,updateTime " \
              "from tss_member_package_history where " \
              "memberPackageId='%s' order by updateTime"
        self.cursor.execute(sql % data["packageId"])
        contents = self.cursor.fetchall()
        # 上一次历史记录临时保存
        last_info = {}
        # 考勤按钮点击次数
        ck_time = 0
        # 所有操作动作集合：
        all_action_list = []
        get_max_num = lambda x, y: abs(x) if abs(x) > abs(y) else abs(y)
        if len(contents) > 0:
            self.resultText.insertPlainText("主会员A：" + contents[0]["memberId"] + "\t\n")
            if len(data["memberIdBind"]) > 30:
                self.resultText.insertPlainText("绑定会员B：" + data["memberIdBind"] + "\t\n")
            for row in contents:
                if len(last_info) == 0:
                    last_info = row
                else:
                    cz_info, class_change_list, fuhao = self.compareClassChange(last_info, row)
                    # 消耗课时
                    class_housr = str(reduce(get_max_num, class_change_list))
                    cz_str = cz_info  # 获取当前可能进行的操作
                    # 去检查其他表是否有此操作
                    kaoqing = re.match(r'[0-9]-[0-9]', cz_str)
                    if "报班" == cz_str:
                        # checkAttendInfo(row, classChangeList)
                        attend_num = attend_num - class_change_list[0]
                        self.saveResultHang(all_action_list, class_housr, cz_str, fuhao, row, None)
                    elif kaoqing is not None:
                        attend_id, member_id, \
                        attendence_status, return_message \
                            = self.checkKaoQing(row, class_change_list, data["memberIdBind"])
                        if attend_id is not None:
                            if len(kaoqing_chongfu_check) > 0 and \
                                    kaoqing_chongfu_check[-1] != cz_str + attend_id + member_id + class_housr:
                                kaoqing_chongfu_check.append(cz_str + attend_id + member_id + class_housr)
                            elif len(kaoqing_chongfu_check) == 0:
                                kaoqing_chongfu_check.append(cz_str + attend_id + member_id + class_housr)
                            elif kaoqing_chongfu_check[-1] == cz_str + attend_id + member_id + class_housr:
                                alert_kaoqing.append(
                                    "警告！" + str(row["updateTime"]) + "\t\n" + "会员： " + member_id + "\t\n"
                                    + " 的班级(报班Id)： " + attend_id + "可能发生 " + cz_str + " 操作重复异常 "
                                    + "\t\n" + "--------------------------------------")
                        ck_time = ck_time + 1
                        ssee = ''
                        if cz_str == "0-1*0-5" and attendence_status == 1:
                            self.saveResultHang(all_action_list, class_housr, "0-1", fuhao, row, return_message)
                        # 判断 0-2 是缺勤还是退班
                        elif cz_str == "0-2" and attendence_status != 2:
                            # 检查是否 有退班记录
                            # self.checkHaveReturnClass(row, data["memberIdBind"])
                            self.saveResultHang(all_action_list, class_housr, "可能是退班操作", fuhao, row, return_message)
                        elif cz_str == "0-2" and attendence_status == 2:
                            self.saveResultHang(all_action_list, class_housr, "0-2", fuhao, row, return_message)
                        elif cz_str == "1-5":
                            if attendence_status == 5:
                                self.saveResultHang(all_action_list, class_housr, "1-5", fuhao, row, return_message)
                            elif attendence_status == 1:
                                self.saveResultHang(all_action_list, class_housr, "5-1", fuhao, row, return_message)
                            elif attendence_status == -1:
                                self.saveResultHang(all_action_list, class_housr, "无操作", fuhao, row, return_message)
                        elif attendence_status == -1:
                            ssee = "\t\n本次未查询到考勤信息，可能存在异常！"
                            self.saveResultHang(all_action_list, class_housr, cz_str, fuhao, row, return_message + ssee)
                        elif cz_str[-1] != attendence_status:
                            ssee = "\t\n本次考勤修改状态为" + str(attendence_status) + "，与课时变化不符，可能存在异常："
                            self.saveResultHang(all_action_list, class_housr, cz_str, fuhao, row, return_message + ssee)
                        else:
                            self.saveResultHang(all_action_list, class_housr, cz_str, fuhao, row, return_message + ssee)
                    elif "退班" == cz_str:
                        self.saveResultHang(all_action_list, class_housr, cz_str, fuhao, row, None)
                    elif "加减课时-加课时" == cz_str:
                        self.saveResultHang(all_action_list, class_housr, cz_str, fuhao, row, None)
                    elif "加减课时-减课时" == cz_str:
                        self.saveResultHang(all_action_list, class_housr, cz_str, fuhao, row, None)
                    elif "未知操作" == cz_str:
                        un_know_oper.append(str(row["updateTime"]))
                        self.saveResultHang(all_action_list, class_housr, cz_str, fuhao, row, None)
                    last_info.clear()
                    last_info = row
        # 开始输出结果
        for k in all_action_list:
            self.resultText.insertPlainText(k + "\t\n")
            self.resultText.insertPlainText("--------------------------------------------------" + "\t\n")
        print("考勤出现次数：" + str(ck_time))
        self.resultText.insertPlainText("报班总课时数：" + str(attend_num) + "\n")
        self.resultText.insertPlainText("考勤操作出现次数：" + str(ck_time) + "\n")
        if len(un_know_oper) > 0:
            self.resultText.insertPlainText("以下时间可能出现多步结果合并异常，请检查：" + "\t\n")
            for un in un_know_oper:
                self.resultText.insertPlainText(un + "\t\n")
        if len(alert_kaoqing) > 0:
            self.resultText.insertPlainText("警告以下异常大概率出现会员重复操作同课节考勤情况，请检查：" + "\t\n")
            for ak in alert_kaoqing:
                self.resultText.insertPlainText(ak + "\t\n")
        if len(un_know_oper) == 0 and len(alert_kaoqing) == 0:
            self.resultText.insertPlainText("没有发现问题")
        self.db.close()

    def saveResultHang(self, all_action_list, class_housr, cz_str, fuhao, row, return_message):
        message = str(row["updateTime"]) + '-> [' + cz_str + ']:' + fuhao + '  ' + '消耗【' + class_housr + '】课时'
        if return_message is not None and len(return_message) > 0:
            message = message + "\t\n" + return_message
        all_action_list.append(message)

    def selectFunction(self, data, i):
        if i == 1:
            # 检查课时包历史记录
            sql = "select memberId " \
                  "from tss_member_package_bind where " \
                  " memberPackageId='%s' and isCancelBind=0 and bindStatus=1  limit 1"
            self.cursor.execute(sql % data["packageId"])
            contents = self.cursor.fetchall()
            if len(contents) > 0:
                data["memberIdBind"] = contents[0]["memberId"]
            else:
                data["memberIdBind"] = ""
            self.checkPackageHistory(data)

    def checkPackage(self):
        self.resultText.clear()
        try:
            db_type = 1
            if self.radioButton.isChecked() is True:
                db_type = 1
            elif self.radioButton_2.isChecked() is True:
                db_type = 3
            elif self.radioButton_3.isChecked() is True:
                db_type = 2
            self.cursor, self.db = bsUtil.getDBLink(db_type)
            memberpackage = self.packageEdit.text()
            if len(memberpackage) < 1:
                self.resultText.clear()
                self.resultText.insertPlainText("请输入课时包Id")
                return
            i = 1
            data = {"packageId": memberpackage}
            self.selectFunction(data, i)
        except Exception as e:
            print(e)
            self.resultText.insertPlainText(e)


if __name__ == "__main__":
    cursor, db = None, None
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
