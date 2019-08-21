import datetime, re

from 补数据专区.bsUtil import getDBLink


def db_init():
    cursor, db = getDBLink(2)
    return db.cursor()


def format_time(str_time):
    tm = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    time_offset = tm - datetime.timedelta(seconds=-1)
    return time_offset.strftime("%Y-%m-%d %H:%M:%S")


def compareNum(first, second):
    if int(first) > int(second):
        return "+"
    elif int(first) == int(second):
        return "="
    else:
        return "-"


def checkOperate(operateStr):
    operateMap = {
        "-+==": "报班",
        "=-+=": "0-1",  # 考勤 或者 0-5
        "+-==": "0-2",  # 退班
        "=-++": "0-3",
        "=-=+": "0-3",
        "+=-=": "1-2",  # 1-2或者 考勤退课 或者 5-2
        "==-+": "1-3",  # 或者 1-6  补课取消考勤 或者5-3
        "===+": "1-6",  # 补课取消考勤
        "-=+=": "2-1",  # 或者 2-5
        "-==+": "2-3",
        "==+1": "3-1",  # 或者 3-5
        "+==-": "3-2",
        "+===": "加课时操作",
        "-===": "减课时操作",
        "===-": "减补课操作",
        "==+-": "减补课操作",
        "====": "无操作"  # 无操作或者1-5 5-1
    }
    if operateStr not in operateMap.keys():
        return "未知操作"
    return operateMap[operateStr]


def compareClassChange(lastInfo, row):
    lastOne = lastInfo["surplusClassHour"]
    lastTwo = lastInfo["unusedClassHour"]
    lastThree = lastInfo["consumptionClassHour"]
    lastFour = lastInfo["remediationClassHour"]
    nowOne = row["surplusClassHour"]
    nowTwo = row["unusedClassHour"]
    nowThree = row["consumptionClassHour"]
    nowFour = row["remediationClassHour"]
    fuhaoOne = compareNum(nowOne, lastOne)
    fuhaoTwo = compareNum(nowTwo, lastTwo)
    fuhaoThree = compareNum(nowThree, lastThree)
    fuhaoFour = compareNum(nowFour, lastFour)
    list = [int(nowOne) - int(lastOne), \
            int(nowTwo) - int(lastTwo), \
            int(nowThree) - int(lastThree), \
            int(nowFour) - int(lastFour) \
            ]
    fuhao = fuhaoOne + fuhaoTwo + fuhaoThree + fuhaoFour
    return checkOperate(fuhao), list, fuhao


def checkAttendInfo(row, list):
    sql = "select ROUND(count(id)*formalClass+giftClass+remedialClass) as classHour " \
          "from tss_member_check_attendance_history where memberId ='2c92828665c3349b0165c361747822ad' " \
          "and updateTime='2018-09-19 16:34:00'"
    pass


def checkKaoQing(row, list, memberIdBind):
    afterTime = format_time(str(row["updateTime"]))
    memberId = row["memberId"]
    sql = "select attendClassId,formalClass,giftClass,remedialClass,updateTime,attendenceStatus  from tss_member_check_attendance_history " \
          "where memberId ='%s' and updateTime = '%s' order by updateTime";
    isFind, attendId = method_checkAttendHistory(afterTime, memberId, row, sql)
    if isFind is not True:
        if len(memberIdBind) < 1:
            print(memberId + "{" + str(row["updateTime"]) + " 会员的考勤 信息未找到}")
        else:
            isBindFind, attendId = method_checkAttendHistory(afterTime, memberIdBind, row, sql)
            if isBindFind is not True:
                print(memberId + "," + memberIdBind + "{" + str(row["updateTime"]) + " 会员的考勤 信息未找到}")
    return attendId


def method_checkAttendHistory(afterTime, memberId, row, sql):
    cursor.execute(sql % (memberId, afterTime))
    result = cursor.fetchall()
    if len(result) > 0:
        for i in result:
            print(i)
            return True, result[0]["attendClassId"]
    else:
        cursor.execute(sql % (memberId, row["updateTime"]))
        result1 = cursor.fetchall()
        if len(result1) > 0:
            for j in result1:
                print(j)
            return True, result1[0]["attendClassId"]
        else:
            return False, None


def checkPackageHistory(data):
    unKnowOper = []
    kaoqingChongfuCheck = []
    alertKaoqing = []
    sql = "select id,memberId,packageName,surplusClassHour,consumptionClassHour," \
          "unusedClassHour,remediationClassHour,updateTime " \
          "from tss_member_package_history where " \
          "memberPackageId='%s' order by updateTime";
    cursor.execute(sql % data["packageId"])
    contents = cursor.fetchall()
    lastInfo = {}
    ckTime = 0
    if len(contents) > 0:
        for row in contents:
            if len(lastInfo) == 0:
                lastInfo = row
            else:
                czInfo, classChangeList, fuhao = compareClassChange(lastInfo, row)
                czStr = czInfo  # 获取当前可能进行的操作
                print(czStr + "   " + fuhao + "   " + str(row["updateTime"]))
                # 去检查其他表是否有此操作
                kaoqing = re.match(r'[0-9]-[0-9]', czStr)
                if "报班" == czStr:
                    pass
                    # checkAttendInfo(row, classChangeList)

                elif kaoqing is not None:
                    attendId = checkKaoQing(row, classChangeList, data["memberIdBind"])
                    if attendId is not None:
                        if len(kaoqingChongfuCheck) > 0 and kaoqingChongfuCheck[-1] != czStr + attendId:
                            kaoqingChongfuCheck.append(czStr + attendId)
                        elif len(kaoqingChongfuCheck) == 0:
                            kaoqingChongfuCheck.append(czStr + attendId)
                        else:
                            alertKaoqing.append("警告！：" + str(row["updateTime"])
                                                + "的班级：" + attendId + "可能发生" + czStr + "操作重复异常")
                    ckTime = ckTime + 1
                elif "出勤变缺勤" == czStr:
                    pass
                elif "退班" == czStr:
                    pass
                elif "加减课时-加课时" == czStr:
                    pass
                elif "加减课时-减课时" == czStr:
                    pass
                elif "无操作" == czStr:
                    pass
                elif "未知操作" == czStr:
                    unKnowOper.append(str(row["updateTime"]))
                print("--------------------------------------------------")
                lastInfo.clear()
                lastInfo = row
    print("考勤出现次数：" + str(ckTime))
    print("以下时间可能出现异常，请检查：")
    for un in unKnowOper:
        print(un)
    for ak in alertKaoqing:
        print(ak)


def selectFunction(i, data):
    if i == 1:
        # 检查课时包历史记录
        sql = "select memberId " \
              "from tss_member_package_bind where " \
              " memberPackageId='%s' and isCancelBind=0 and bindStatus=1 order by updateTime desc limit 1";
        cursor.execute(sql % data["packageId"])
        contents = cursor.fetchall()
        if len(contents)>0:
            data["memberIdBind"] = contents[0]["memberId"]
        else:
            data["memberIdBind"] = ""
        checkPackageHistory(data)


if __name__ == '__main__':
    print("bug查找快捷启动...")
    cursor = db_init()
    i = 1
    data = {"packageId": "2c9282826afeb058016b0cd2dcbf0c16"}
    selectFunction(i, data)
