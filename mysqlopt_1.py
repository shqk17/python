import pymysql, datetime

db = pymysql.connect(host='192.168.0.5',
                     port=3306,
                     user='root',
                     passwd='asdfg_qwert@',
                     db='tss',
                     charset='utf8'
                     # , cursorclass=pymysql.cursors.DictCursor
                     )
cursor = db.cursor()

tableName = ['tss_member_add_subtract_record',
             'tss_member_attend_class_record',
             'tss_member_check_attendance',
             'tss_member_check_attendance_history',
             'tss_member_follow_up_record',
             'tss_member_package',
             'tss_member_package_attend_class',
             'tss_member_package_history',
             'tss_member_return_class_record'
             ]
sql = "SELECT * from ( SELECT a.id ,a.memberId, a.schoolId as AschoolId,b.schoolId " \
      "from (select a.id,a.memberId,c.schoolId from %s a LEFT JOIN " \
      "tss_student b on a.memberId =b.id LEFT JOIN sys_admin_user c on b.adminUserId =c.id )a " \
      "LEFT JOIN ( select a.id,b.schoolId from %s a LEFT JOIN " \
      "sys_admin_user b on a.adminUserId =b.id ) b on a.id = b.id ) a " \
      "where a.AschoolId != a.schoolId and a.schoolId is not null and  a.schoolId !=''  and a.AschoolId !='';"
schoolMap = {}
for x in tableName:
    try:
        print(sql % (x, x))
        cursor.execute(sql % (x, x))
        contents = cursor.fetchall()
        ids = []
        if len(contents) > 0:
            for row in contents:
                ids.append(row[1])
        schoolMap[x] = ids
    except Exception as e:
        print(e)
for k, v in schoolMap.items():
    print(k + ":" + ",".join(v))

# 遍历所有的memberId 分别是在哪个地方出错
studentIdInfo = schoolMap['tss_member_package_history']


def addSubFrom(studentid):
    sql = "select createTime from tss_member_add_subtract_record where memberId='%s'"
    cursor.execute(sql % (studentid))
    addSubFrom_contents = cursor.fetchall()
    timeList = []
    timestr = "1"
    if len(addSubFrom_contents) > 0:
        for row in addSubFrom_contents:
            timeList.append(row[0])
    if len(timeList) == 0:
        print(studentid + "没有在加减课时表里找到错误记录！！！！！！")
    elif len(timeList) > 1:
        print(studentid + "在加减课时表里找到多条错误记录_" + str(len(timeList)))
        timestr = str(timeList[0])
    elif len(timeList) == 1:
        timestr = str(timeList[0])
    print(timestr)
    if len(timestr) > 1:
        doFinish(studentid, "加减课时表", timestr)


def doFinish(studentid, tableName, timestr):
    sql = "select * from sys_handle_log  " \
          "where requestTime>='%s' " \
          "and requestTime<='%s' " \
          "and  adminUserId  in " \
          "(select id from sys_admin_user where " \
          "schoolId =( select c.id from tss_student a " \
          "left join sys_admin_user b on a.adminUserId =b.id" \
          " left join sys_school c on b.schoolId = c.id where a.id ='%s'))"
    Starttime = timestr.split(" ")[0] + " 00:00:01"
    endtime = timestr.split(" ")[0] + " 23:59:59"
    cursor.execute(sql % (Starttime, endtime, studentid))
    mySchoolStaffInfo = cursor.fetchall()
    if len(mySchoolStaffInfo) > 0:
        print("用户" + studentid + "----所属园所老师在当天有操作信息：需要进一步确认，时间：" + Starttime + "____" + endtime)
        flieLog = open("./checkBug.txt", "a")
        flieLog.write(
            "用户" + studentid + "----所属园所老师在当天有操作信息：需要进一步确认，时间：" + Starttime + "____" + endtime + "\n" + str(
                sql % (Starttime, endtime, studentid)))
        flieLog.close()
        # 进一步检查
        day = datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
        st = (day + datetime.timedelta(minutes=-5)).strftime("%Y-%m-%d %H:%M:%S")
        sb = (day + datetime.timedelta(minutes=+5)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(sql % (st, sb, studentid))
        mySchoolStaffInfo_2 = cursor.fetchall()
        if len(mySchoolStaffInfo_2) > 0:
            print("用户" + studentid + "----所属园所老师在有操作信息：需要最终确认，时间：" + st + "____" + sb)
            flieLog = open("./checkBug.txt", "a")
            flieLog.write("用户" + studentid + "----所属园所老师在当天有操作信息：需要最终确认，时间：" + st + "____" + sb + "\n" + str(
                sql % (Starttime, endtime, studentid)))
            flieLog.close()
            finalFile = open("./finalFile.txt", "a")
            finalFile.write("用户" + studentid + "_" + tableName + "_是本园所操作\n")
            flieLog.close()
        else:
            finalFile = open("./finalFile.txt", "a")
            finalFile.write("用户" + studentid + "_" + tableName + "可能是本园所操作\n")
            finalFile.close()
    else:
        finalFile = open("./finalFile.txt", "a")
        finalFile.write("用户" + studentid + "_" + tableName + "不是本园所操作")
        finalFile.close()


def attendFrom(studentid):
    sql = "select createTime from tss_member_package_attend_class where memberId='%s'"
    cursor.execute(sql % (studentid))
    attendFrom_contents = cursor.fetchall()
    timeList = []
    timestr = "1"
    if len(attendFrom_contents) > 0:
        for row in attendFrom_contents:
            timeList.append(row[0])
    if len(timeList) == 0:
        print(studentid + "没有在报班课时表里找到错误记录！！！！！！")
    elif len(timeList) > 1:
        print(studentid + "在报班课时表里找到多条错误记录_" + str(len(timeList)))
        timestr = str(timeList[0])
    elif len(timeList) == 1:
        timestr = str(timeList[0])
    print(timestr)
    if len(timestr) > 1:
        doFinish(studentid, "报班表", timestr)


def followFrom(studentid):
    sql = "select createTime from tss_member_follow_up_record where memberId='%s'"
    cursor.execute(sql % (studentid))
    followFrom_contents = cursor.fetchall()
    timeList = []
    timestr = "1"
    if len(followFrom_contents) > 0:
        for row in followFrom_contents:
            timeList.append(row[0])
    if len(timeList) == 0:
        print(studentid + "没有在跟进表里找到错误记录！！！！！！")
    elif len(timeList) > 1:
        print(studentid + "在跟进表里找到多条错误记录_" + str(len(timeList)))
        timestr = str(timeList[0])
    elif len(timeList) == 1:
        timestr = str(timeList[0])
    print(timestr)
    if len(timestr) > 1:
        doFinish(studentid, "跟进表", timestr)


for studentid in studentIdInfo:
    # 第一步加减课时 判断：
    if studentid in ",".join(schoolMap['tss_member_add_subtract_record']):
        addSubFrom(studentid);
    # 第二步考勤 判断：
    elif studentid in ",".join(schoolMap['tss_member_attend_class_record']):
        attendFrom(studentid)
    elif studentid in ",".join(schoolMap['tss_member_follow_up_record']):
        followFrom(studentid)
    else:
        print("----未知from——error：" + studentid)

cursor.close()
db.close()
print('请输入任意键结束：')
input()
