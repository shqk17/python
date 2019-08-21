import uuid

from 补数据专区 import bsUtil

cursor, db = bsUtil.getDBLink(1)

sql = " SELECT	a.id as appointmentId,	a.studentId as memberId,	a.adminUserId ," \
      "	a.isAttendance as attendStatus, 	a.createTime,	a.updateTime, 	b.schoolId " \
      "FROM	tss_app_appointment_manage a	LEFT JOIN tss_student b ON a.studentId = b.id " \
      "WHERE	a.type =2"
cursor.execute(sql)
contents = cursor.fetchall()

insertSql = "INSERT INTO `tss_activity_attend_history`(`id`, `appointmentId`,`memberId`, `adminUserId`, " \
            "`attendStatus`,`createTime`,  `version`,`updateTime`,`isRecordStatic`, `schoolId`) VALUES (" \
            "'%s'," \
            " '%s', '%s', '%s'" \
            " ,%s, '%s', 0,'%s',1,'%s');"
for s in contents:
    sqq = insertSql % (str(uuid.uuid4()).replace("-", ""),
                       s[0],
                       s[1],
                       s[2],
                       s[3],
                       s[4],
                       s[5],
                       s[6])
    sdsd = sqq.replace("'None'", "Null")
    print(sdsd)
    cursor.execute(sdsd)

cursor.close()
db.commit()
db.close()
