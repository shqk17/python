import pymysql, datetime, uuid, time

# db = pymysql.connect(host='hb3-rds20180919.mysql.zhangbei.rds.aliyuncs.com',
#                      port=3382,
#                      user='qms',
#                      passwd='rybu0OsWO2qL7Ef',
#                      db='tss',
#                      charset='utf8'
#                      #, cursorclass=pymysql.cursors.DictCursor
#                      )
#
db = pymysql.connect(host='192.168.0.34',
                     port=3306,
                     user='root',
                     passwd='Aa12345678',
                     db='tss',
                     charset='utf8'
                     # , cursorclass=pymysql.cursors.DictCursor
                     )
#
# db = pymysql.connect(host='127.0.0.1',
#                      port=3306,
#                      user='root',
#                      passwd='aa123567',
#                      db='tss',
#                      charset='utf8'
#                      # , cursorclass=pymysql.cursors.DictCursor
#                      )
cursor = db.cursor()

sql = "SELECT DISTINCT a.memberId,c.schoolName FROM tss_member_check_attendance_history a  " \
      "	LEFT JOIN tss_student b on a.memberId =b.id " \
      "	LEFT JOIN sys_school c on b.schoolId =c.id " \
      "WHERE" \
      "	a.attendenceStatus <> 0" \
      "	AND a.memberId IN ( SELECT memberId FROM tss_member_package_bind ) and c.schoolName !='线上测试投资' and c.schoolName!='线上测试园2督导专用' and a.remedialClass<1" \
      "	ORDER BY a.updateTime "
cursor.execute(sql)
contents = cursor.fetchall()

kaoqingMap = []
kaoqingBkMap = []
kqSql = "SELECT a.memberId,b.memberPackageId,count(a.id)*a.formalClass as formal , count(a.id)*a.giftClass as gift 	FROM tss_member_check_attendance a 	LEFT JOIN tss_member_package_attend_class b on b.memberAttendClassId  =  a.attendClassId 	WHERE a.memberId = '%s' and a.attendenceStatus in(1,5) GROUP BY b.memberPackageId ORDER BY a.updateTime;"

kqSqlBk = "SELECT a.memberId,b.memberPackageId,count(a.id)*a.formalClass as formal , count(a.id)*a.giftClass as gift 	FROM tss_member_check_attendance a 	LEFT JOIN tss_member_package_attend_class b on b.memberAttendClassId  =  a.attendClassId 	WHERE a.memberId = '%s' and a.attendenceStatus=3 and  updateTime<='2019-05-29 00:00:00' GROUP BY b.memberPackageId ORDER BY a.updateTime;"


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



def suoyin(amap):
    newmap = {}
    for x in amap:
        newmap[str(x[0]) + "-" + str(x[1])] = x
    return newmap


a_kq = suoyin(kaoqingMap)
a_kqbk = suoyin(kaoqingBkMap)

a_hd = suoyin(hdMap)

# a_jj = suoyin(jjMap)


def hebing_1(A, B):
    for k, v, in B.items():
        if A.__contains__(k):
            # 做加的操作：
            sss = A[k][2] + v[2]
            A[k] = tuple([A[k][0], A[k][1], sss, A[k][3]])
        else:
            A[k] = v
    return A


def hebing_2(A, B):
    for k, v, in B.items():
        if A.__contains__(k):
            # 做加的操作：
            sss = A[k][2] + v[2]
            mmm = A[k][3] + v[3]
            A[k] = tuple([A[k][0], A[k][1], sss, mmm])
        else:
            A[k] = v
    return A


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


def bijiao(A, B):
    i = 0
    for k, v, in B.items():
        if A.__contains__(k):
            # 做加的操作：
            if float('%.2f' % A[k][2]) != float('%.2f' % v[2]) or float('%.2f' % A[k][3]) != float('%.2f' % v[3]):
                print("-------start--------")
                print(A[k])
                print(B[k])
                print("-------end--------")
                i = i + 1
    print(i)


bijiao(bjList, a_kq)

cursor.close()
db.close()

print('请输入任意键结束：')
input()
