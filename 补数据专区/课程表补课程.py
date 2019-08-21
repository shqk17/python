import pymysql, datetime, uuid, time

db = pymysql.connect(host='hb3-rds20180919.mysql.zhangbei.rds.aliyuncs.com',
                     port=3382,
                     user='qms',
                     passwd='rybu0OsWO2qL7Ef',
                     db='tss',
                     charset='utf8'
                     #, cursorclass=pymysql.cursors.DictCursor
                     )
#
# db = pymysql.connect(host='192.168.0.5',
#                      port=3306,
#                      user='root',
#                      passwd='asdfg_qwert@',
#                      db='tss',
#                      charset='utf8'
#                      # , cursorclass=pymysql.cursors.DictCursor
#                      )

# db = pymysql.connect(host='127.0.0.1',
#                      port=3306,
#                      user='root',
#                      passwd='aa123567',
#                      db='tss',
#                      charset='utf8'
#                      # , cursorclass=pymysql.cursors.DictCursor
#                      )
cursor = db.cursor()

noFoundAdmin = []

classInfo = ["4e80b7f07a584e29b1b022f6c1af0b6d",
             "62088fda936c41c6b2e8b4f6c6edb788",
             "70554ef508274b81804d385fb4082a94",
             "b4edf0af1bd0431f962604e35e7e5ac6"]

sql = "select id ,schoolName,schoolProvince,schoolCity,schoolRegion,schoolAddress" \
      ",latitude,longitude,type from sys_school "
cursor.execute(sql)
contents = cursor.fetchall()
courseIdSql = "SELECT * from tss_course where adminUserId in (SELECT id from sys_admin_user where schoolId ='%s') and systemPid ='6c2c4094c1d64dff8a47e8ca26b4eed0'"
getAdminBySchool = "select id from sys_admin_user where schoolId ='%s' and post in (1,2,12) and userPassword is not null order by post limit 1"
insertClass = "INSERT INTO `tss`.`tss_course`(`id`, `systemId`, `systemPid`, `adminUserId`, `type`" \
              ", `status`, `createTime`, `updateTime`, `version`, `isBlockUp`, `trialAge`, `trialAgeStart`, `trialAgeEnd`, 'isDeleted')" \
              " VALUES ('%s', " \
              "'%s'," \
              " '6c2c4094c1d64dff8a47e8ca26b4eed0', " \
              "'%s'," \
              " 1, NULL, '2019-07-31 09:25:12', '2019-07-31 09:25:12', 1, b'0', NULL, NULL, NULL ,0);"
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
                insetsqls = (insertClass % (str(uuid.uuid4()).replace("-", ""), i, admins[0][0]))
                print(insetsqls)
                # cursor.execute(insetsqls)
        else:
            noFoundAdmin.append(s)

for ss in noFoundAdmin:
    print(ss in + ':的管理员没找到')
cursor.close()
# db.commit()
db.close()

print('请输入任意键结束：')
input()
