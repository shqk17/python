import pymysql, datetime


def db_init():
    db = pymysql.connect(host='192.168.0.5',
                         port=3306,
                         user='root',
                         passwd='asdfg_qwert@',
                         db='tss',
                         charset='utf8'
                         , cursorclass=pymysql.cursors.DictCursor
                         )
    return db.cursor()


def compareNum(first, second):
    if int(first) > int(second):
        return "+"
    elif int(first) == int(second):
        return "="
    else:
        return "-"


def checkOperate(operateStr):
    operateMap = {
        "-=+=": "报班",
        "=+-=": "考勤",
        "+=-=": "出勤变缺勤",
        "+=--": "退班",
        "+===": "加减课时-加课时",
        "-===": "加减课时-减课时",
        "====": "无操作"
    }
    if operateStr not in operateMap.keys():
        return "未知操作"
    return operateMap[operateStr]


def compareClassChange(lastInfo, row):
    lastOne = lastInfo["surplusClassHour"]
    lastTwo = lastInfo["consumptionClassHour"]
    lastThree = lastInfo["unusedClassHour"]
    lastFour = lastInfo["selectedClassHour"]
    nowOne = row["surplusClassHour"]
    nowTwo = row["consumptionClassHour"]
    nowThree = row["unusedClassHour"]
    nowFour = row["selectedClassHour"]
    fuhaoOne = compareNum(nowOne, lastOne)
    fuhaoTwo = compareNum(nowTwo, lastTwo)
    fuhaoThree = compareNum(nowThree, lastThree)
    fuhaoFour = compareNum(nowFour, lastFour)
    list = [int(nowOne) - int(lastOne), \
            int(nowTwo) - int(lastTwo), \
            int(nowThree) - int(lastThree), \
            int(nowFour) - int(lastFour)]
    return checkOperate(
        fuhaoOne + fuhaoTwo + fuhaoThree + fuhaoFour), list


def checkAttendInfo(row, list):
    sql = "select ROUND(count(id)*formalClass+giftClass+remedialClass) as classHour " \
          "from tss_member_check_attendance_history where memberId ='2c92828665c3349b0165c361747822ad' " \
          "and updateTime='2018-09-19 16:34:00'"
    pass


def checkKaoQing(row, list):
    sql = "select (formalClass+giftClass+remedialClass) as classHour from tss_member_check_attendance_history " \
          "where memberId ='2c92828665c3349b0165c361747822ad' and operatingTime = '' order by updateTime";


def checkPackageHistory(packageId):
    sql = "select id,memberId,packageName,surplusClassHour,consumptionClassHour,unusedClassHour,remediationClassHour,selectedClassHour from tss_member_package_history where memberPackageId='2c92828665c3349b0165c361749822b0' order by updateTime";
    cursor.execute(sql)
    contents = cursor.fetchall()
    lastInfo = {}
    if len(contents) > 0:
        for row in contents:
            if len(lastInfo) == 0:
                lastInfo = row
            else:
                czInfo = compareClassChange(lastInfo, row)
                czStr = czInfo[0]  # 获取当前可能进行的操作
                print(czStr)
                # 去检查其他表是否有此操作
                if "报班" == czStr:
                    checkAttendInfo(row, list)
                elif "考勤" == czStr:
                    checkKaoQing(row, list)
                elif "出勤变缺勤" == czStr:
                    pass
                elif "退班" == czStr:
                    pass
                elif "加减课时-加课时" == czStr:
                    pass
                elif "加减课时-减课时" == czStr:
                    pass
                elif "无操作" == czStr or "未知操作" == czStr:
                    pass
                lastInfo.clear()
                lastInfo = row


def selectFunction(i, data):
    if i == 1:
        # 检查课时包历史记录
        checkPackageHistory(data["packageId"])


if __name__ == '__main__':
    print("bug查找快捷启动...")
    cursor = db_init()
    i = 1
    data = {"packageId": "2c928286686134740168d1498a163845"}
    selectFunction(i, data)
