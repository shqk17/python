import pymysql, datetime, uuid, time

from 补数据专区 import bsUtil

cursor, db = bsUtil.getDBLink(1)

sql = "SELECT 	a.memberId,	b.memberPackageId,	sum(a.formalClass) AS formal,	sum(a.giftClass) AS gift FROM	tss_member_check_attendance a" \
      " LEFT JOIN tss_member_package_attend_class b ON b.memberAttendClassId = a.attendClassId WHERE" \
      " a.memberId IN ( SELECT DISTINCT memberId FROM tss_member_package_bind )" \
      " AND a.attendenceStatus = 0" \
      "	AND a.isDelete = 0 GROUP BY	b.memberPackageId ,a.memberId ORDER BY	a.updateTime;"
cursor.execute(sql)
contents = cursor.fetchall()

sql2 = "select memberId,memberPackageId, binderPositiveUnusedClassHour,binderGiftUnusedClassHour from " \
       "tss_member_package_bind "
cursor.execute(sql2)
contents2 = cursor.fetchall()


newMap = bsUtil.suoyin(contents)
oldMap = bsUtil.suoyin(contents2)

bsUtil.bijiao2(oldMap,newMap)

cursor.close()
db.close()

print('请输入任意键结束：')
input()
