import pymysql, datetime, uuid, time
from bsUtil import *

cursor, db = getDBLink(1)

sql = "SELECT DISTINCT a.memberId,c.schoolName FROM tss_member_check_attendance_history a  " \
      "	LEFT JOIN tss_student b on a.memberId =b.id " \
      "	LEFT JOIN sys_school c on b.schoolId =c.id " \
      "WHERE" \
      "	a.attendenceStatus <> 0" \
      "	AND a.memberId IN ( SELECT memberId FROM tss_member_package_bind )  and c.schoolName!='线上测试园2督导专用' and a.remedialClass<1" \
      "	ORDER BY a.updateTime "
cursor.execute(sql)
contents = cursor.fetchall()

kaoqingMap = []
kaoqingBkMap = []
kqSql = "SELECT a.memberId,b.memberPackageId,sum(a.formalClass) as formal , sum(a.giftClass) as gift 	FROM tss_member_check_attendance a 	LEFT JOIN tss_member_package_attend_class b on b.memberAttendClassId  =  a.attendClassId 	WHERE a.memberId = '%s' and a.attendenceStatus in(1,5) GROUP BY b.memberPackageId ORDER BY a.updateTime;"

kqSqlBk = "SELECT a.memberId,b.memberPackageId,sum(a.formalClass) as formal , sum(a.giftClass) as gift 	FROM tss_member_check_attendance a 	LEFT JOIN tss_member_package_attend_class b on b.memberAttendClassId  =  a.attendClassId 	WHERE a.memberId = '%s' and a.attendenceStatus=3 and  updateTime<='2019-05-29 00:00:00' GROUP BY b.memberPackageId ORDER BY a.updateTime;"

for s in contents:
    cursor.execute(kqSql % s[0])
    kq = cursor.fetchall()
    if len(kq) > 0:
        for ss in kq:
            kaoqingMap.append(ss)
        print("发现考勤信息：" + s[0])
for s in contents:
    cursor.execute(kqSqlBk % s[0])
    kqbk = cursor.fetchall()
    if len(kq) > 0:
        for ss in kq:
            kaoqingBkMap.append(ss)
        print("发现考勤补课信息：" + s[0])

hdSql = "SELECT a.studentId as memberId,a.memberPackageId,sum(a.formalClassHour) as formal	from tss_app_appointment_manage a	LEFT JOIN tss_student b on a.studentId =b.id LEFT JOIN sys_school c on b.schoolId =c.id 	WHERE a.type=2 and a.isAttendance =1 and studentType=1 and memberPackageId is not null and  a.studentId in (SELECT DISTINCT memberId FROM tss_member_package_bind) and c.schoolName !='线上测试投资'	GROUP BY a.studentId ;"
cursor.execute(hdSql)
hdMap = cursor.fetchall()

# jiajianSql = "SELECT aa.memberId,aa.memberPackageId,	IFNULL( CASE classHourType WHEN 1 THEN comClassHour END, 0 ) AS formal,	ifnull( CASE classHourType WHEN 2 THEN comClassHour END, 0 ) AS gift FROM 	( 	SELECT	a.memberId,	a.memberPackageId,a.classHourType,sum( a.classHour ) AS comClassHour FROM tss_member_add_subtract_record a LEFT JOIN tss_student b ON a.memberId = b.id	LEFT JOIN sys_school c ON b.schoolId = c.id	WHERE a.addSubtractType = 2	AND a.classHourType BETWEEN 1 AND 2 AND a.memberId IN ( SELECT DISTINCT memberId FROM tss_member_package_bind )	AND c.schoolName != '线上测试投资' GROUP BY	a.memberId,	a.memberPackageId,a.classHourType) aa GROUP BY aa.memberId,aa.memberPackageId"
# cursor.execute(jiajianSql)
# jjMap = cursor.fetchall()

a_kq = suoyin(kaoqingMap)
a_kqbk = suoyin(kaoqingBkMap)

a_hd = suoyin(hdMap)

# a_jj = suoyin(jjMap)

a_kq = hebing_1(a_kq, a_kqbk)
a_kq = hebing_1(a_kq, a_hd)
# a_kq = hebing_2(a_kq, a_jj)

for x, y in a_kq.items():
    print(str(x) + ":" + str(y))

bjiaoSql = "select memberId ,memberPackageId,binderPositiveConsumptionClassHour as formal ," \
           "binderGiftConsumptionClassHour as gift from tss_member_package_bind "

cursor.execute(bjiaoSql)
bjMap = cursor.fetchall()
bjList = suoyin(bjMap)

bijiao(bjList, a_kq)

cursor.close()
db.close()

print('请输入任意键结束：')
input()
