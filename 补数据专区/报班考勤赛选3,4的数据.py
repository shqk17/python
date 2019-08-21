import pymysql, datetime, uuid, time

from 补数据专区 import bsUtil

cursor, db = bsUtil.getDBLink(1)

sql = "SELECT * from (" \
      "	SELECT a.id,a.memberId,a.checkAttendanceId,a.updateTime,GROUP_CONCAT( attendenceStatus ) as statuss	from (" \
      "SELECT id,memberId, checkAttendanceId, updateTime, ROUND(attendenceStatus) as attendenceStatus FROM tss_member_check_attendance_history WHERE isDelete = 0 AND attendenceStatus <> 0" \
      ") a GROUP BY a.memberId, a.checkAttendanceId HAVING count(a.id)>1 )b where b.statuss like '%3%' and b.statuss like '%4%'"
cursor.execute(sql)
contents = cursor.fetchall()

sql2 = "SELECT * from (SELECT *,GROUP_CONCAT(ROUND(attendenceStatus)) as statuss from tss_member_check_attendance_history " \
       "where memberId='%s' and checkAttendanceId='%s' ORDER BY updateTime)a where a.statuss like '\%3,4\%'"

result = []
for i in contents:
    print(i)
    print(i[1])
    print(i[2])
    print(i[3])
    print(sql2 % (i[1], i[2]))
    cursor.execute(sql2 % (i[1], i[2]))
    contents2 = cursor.fetchall()
    if len(contents2) > 0:
        print("find one :" + str(i))
        result.append(i)

back = open("./考勤有3,4的问题.txt", encoding="utf-8", mode='a')
for s in result:
    back.write(str(s) + "\n")
back.flush()
cursor.close()
db.close()

print('请输入任意键结束：')
input()
