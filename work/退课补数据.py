import pymysql, datetime, uuid, time

from 补数据专区.bsUtil import getDBLink

sql = "SELECT aa.* ,d.schoolName from (SELECT a.* ,sum(b.amount) as amount  " \
      "from tss_member_check_attendance_history a LEFT JOIN " \
      "tss_right_statistic b on a.checkAttendanceId = b.attendanceId" \
      " where a.attendenceStatus =4  and  b.isDelete=0 GROUP BY a.checkAttendanceId )aa" \
      " LEFT JOIN sys_admin_user c on c.id = aa.adminUserId LEFT JOIN" \
      " sys_school d on d.id =c.schoolId where  aa.amount !=0.00 and" \
      " d.schoolName not in ('线上测试投资','线上测试园2督导专用') "
cursor, db = getDBLink(1)
cursor.execute(sql)
contents = cursor.fetchall()

courseIdSql = "SELECT * from tss_right_statistic where attendanceId ='%s' and isDelete =0"
one = 0
for s in contents:
    cursor.execute(courseIdSql % s[1])
    courseIds = cursor.fetchall()
    if (courseIds is not None and len(courseIds) == 1):
        print(s[1] + " is 只有一条")
        one += 1
        insetSql = "INSERT INTO `tss`.`tss_right_statistic`(`id`, `stuId`, `type`, `responsibilityType`, " \
                   "`attendanceId`, `paymentId`, `returnPremiumId`, `memberPackageId`, `amount`, `adminUserId`, " \
                   "`isDelete`, `createTime`, `updateTime`, `version`, `appointmentManageId`, `addsubtractId`, " \
                   "`supplementaryTime`, `importTime`) VALUES (" \
                   "'%s', " \
                   "'%s', " \
                   "%d, %d, '%s', " \
                   "%s, %s, %s, %s, " \
                   "'%s'," \
                   " %d, '%s', '%s', %d, %s, %s, %s, %s);"
        ss = list(courseIds[0])
        ss[0] = str(uuid.uuid4()).replace("-", "")
        ss[3] = 2
        ss[8] = -float('%.2f' % ss[8])
        instsql = insetSql % tuple(ss)
        print(instsql.replace("None", "Null"))
        cursor.execute(instsql.replace("None", "Null"))
    else:
        print(s[1] + " is 有" + str(len(courseIds)))
print(one)

cursor.close()
db.commit()
db.close()

print('请输入任意键结束：')
input()
