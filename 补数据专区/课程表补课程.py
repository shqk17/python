import pymysql, datetime, uuid, time

db = pymysql.connect(host='hb3-rds20180919.mysql.zhangbei.rds.aliyuncs.com',
                     port=3382,
                     user='qms',
                     passwd='rybu0OsWO2qL7Ef',
                     db='tss',
                     charset='utf8'
                     #, cursorclass=pymysql.cursors.DictCursor
                     )

# db = pymysql.connect(host='192.168.0.34',
#                      port=3306,
#                      user='root',
#                      passwd='Aa12345678',
#                      db='tss',
#                      charset='utf8'
#                      # , cursorclass=pymysql.cursors.DictCursor
#                      )
# db = pymysql.connect(host='192.168.0.5',
#                              port=3306,
#                              user='root',
#                              passwd='asdfg_qwert@',
#                              db='tss',
#                              charset='utf8'
#                               # , cursorclass=pymysql.cursors.DictCursor
#                              )
cursor = db.cursor()

noFoundAdmin = []

classInfo = ["a957c423c0094819b1fc216b3cc22508",
             "fc1262a098ec474d9ab66de64c1f33d7",
             "299a93d3d2fc4be180772d3754b8f8e7",
             "bb00863d297d45d783a84be798c2a46e",
             "77326cdbaf3e490e9f4a29fcc0f3cbae"]

sql = "select id ,schoolName,schoolProvince,schoolCity,schoolRegion,schoolAddress" \
      ",latitude,longitude,type from sys_school where type = 3 "
cursor.execute(sql)
contents = cursor.fetchall()
courseIdSql = "SELECT * from tss_course where adminUserId in (SELECT id from sys_admin_user where schoolId ='%s') and systemPid ='8d0c34c5ced841ac8068250fdfbcd4fa'"
getAdminBySchool = "select id from sys_admin_user where schoolId ='%s' and post in (1,2,12) and userPassword is not null order by post limit 1"
insertClass = "INSERT INTO `tss`.`tss_course`(`id`, `systemId`, `systemPid`, `adminUserId`, `type`" \
              ", `status`, `createTime`, `updateTime`, `version`, `isBlockUp`, `trialAge`, `trialAgeStart`, `trialAgeEnd`,  `isDeleted`,`sacType`)" \
              " VALUES ('%s', " \
              "'%s'," \
              " '8d0c34c5ced841ac8068250fdfbcd4fa', " \
              "'%s'," \
              " 1, NULL, '2019-07-31 09:25:12', '2019-07-31 09:25:12', 1, b'0', NULL, NULL, NULL ,0,'%s');"
for s in contents:
    cursor.execute(courseIdSql % s[0])
    courseIds = cursor.fetchall()
    if (courseIds is not None and len(courseIds) > 0):
        print(s[1] + " is ok")
    else:
        cursor.execute(getAdminBySchool % s[0])
        admins = cursor.fetchall()
        if (admins is not None and len(admins) > 0):
            for i in classInfo:
                insetsqls_D = (insertClass % (str(uuid.uuid4()).replace("-", ""), i, admins[0][0], 'D,C,W'))
                print(insetsqls_D)
                print("--------------------------------")
                cursor.execute(insetsqls_D)
        else:
            noFoundAdmin.append(s)

for ss in noFoundAdmin:
    print(ss in + ':的管理员没找到')
cursor.close()
db.commit()
db.close()

print('请输入任意键结束：')
input()
