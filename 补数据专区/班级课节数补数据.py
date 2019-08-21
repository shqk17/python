import pymysql, datetime, uuid, time, queue, threading
from time import sleep, ctime
from 补数据专区 import bsUtil, xiancheng

cursor, db = bsUtil.getDBLink(3)

sql = "SELECT a.*,b.surplusPitchNumber from ( SELECT classId,COUNT(1) as snum FROM tss_class_lessons " \
      "WHERE CONCAT(classTime,' ',startTime) >= NOW()  AND `status` =1 " \
      "and adminUserId in (SELECT id from sys_admin_user where schoolId ='2c9215846afeb088016b06c7d7921ad3') " \
      "group by classId) a LEFT JOIN tss_classes b on a.classId=b.id where  b.surplusPitchNumber!=a.snum"
cursor.execute(sql)
contents = cursor.fetchall()
updateSql = "update tss_classes set surplusPitchNumber =%s where id ='%s' "
if len(contents)<1:
    print("没有错误数据")
else:
    for i in contents:
        print(updateSql % (i[1], i[0]))
        cursor.execute(updateSql % (i[1], i[0]))
cursor.close()
db.commit()
db.close()

print('请输入任意键结束：')
input()
