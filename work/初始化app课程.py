import pymysql, datetime , uuid ,time
#
# db = pymysql.connect(host='hb3-rds20180919.mysql.zhangbei.rds.aliyuncs.com',
#                      port=3382,
#                      user='qms',
#                      passwd='rybu0OsWO2qL7Ef',
#                      db='tss',
#                      charset='utf8'
#                      #, cursorclass=pymysql.cursors.DictCursor
#                      )

db = pymysql.connect(host='192.168.0.5',
                     port=3306,
                     user='root',
                     passwd='asdfg_qwert@',
                     db='tss',
                     charset='utf8'
                     # , cursorclass=pymysql.cursors.DictCursor
                     )

# db = pymysql.connect(host='127.0.0.1',
#                      port=3306,
#                      user='root',
#                      passwd='aa123567',
#                      db='tss',
#                      charset='utf8'
#                      # , cursorclass=pymysql.cursors.DictCursor
#                      )
cursor = db.cursor()

sql = "select id ,schoolName,schoolProvince,schoolCity,schoolRegion,schoolAddress" \
      ",latitude,longitude,type from sys_school "
cursor.execute(sql)
contents = cursor.fetchall()
schoolInfo = []
noCourseSchool = []
courseIdSql = "SELECT * from tss_app_course where adminUserId in (SELECT id from sys_admin_user WHERE schoolId ='%s')"
for s in contents:
    schoolInfo.append(s)
    cursor.execute(courseIdSql % s[0])
    courseIds = cursor.fetchall()
    if (courseIds is not None and len(courseIds) > 0):
        print(s[1] + " is ok")
    elif s[8] != 3:
        noCourseSchool.append(s)
print(noCourseSchool)
print(len(noCourseSchool))
getAdminBySchool = "select id from sys_admin_user where schoolId ='%s' and post in (1,2,12) order by post limit 1"

sysconSql = "select * from sys_config where groupId='ff808081643f34610164456068ef18ed' and name !='c62164b84dab46e4b0484f249d0e2e87' and  name !='195c234ed2ff424cbb4ad8829f4d6ad6' and name !='e14765a134634818889e54b17401d05b'"
cursor.execute(sysconSql)
sysconf = cursor.fetchall()
if len(sysconf)>0:
    pass
else:
    print("配置异常！！！")
    print('请输入任意键结束：')
    input()
intsetCourse ="INSERT INTO `tss`.`tss_app_course`(`id`, `courseSystemId`, `courseSystemPid`, `publicityImage`, `addressProvince`, `addressCity`, `addressRegion`, `address`, `activityDetails`, `issue`, `adminUserId`, `latitude`, `longitude`, `createTime`, `updateTime`, `version`) VALUES ('%s', NULL, '%s', '%s', '%s', '%s', '%s', '%s', '', 2, '%s', %s, %s, '%s', '%s', 0);"


def initTssClasses(school, adminId):
    timestamp = time.time()
    timestruct = time.localtime(timestamp)
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", timestruct)
    print(nowTime)
    print('开始初始化-'+school[1])
    for conf in sysconf:
        newsql = intsetCourse % (str(uuid.uuid4()).replace("-",""),
                                       conf[1],
                                       conf[2],
                                       school[2],
                                       school[3],
                                       school[4],
                                       school[5],
                                       adminId,
                                       school[6], # if(school[6] is not None) else Null
                                       school[7],
                                       nowTime,
                                       nowTime)
        isql = newsql.replace("None","Null")
        print(isql)
        cursor.execute(isql)



for school in noCourseSchool:
    cursor.execute(getAdminBySchool % school[0])
    adminIds = cursor.fetchall()
    if len(adminIds) > 0:
        adminId = adminIds[0][0]
        print("园所 ： " + school[1] + "管理员ID：" + adminId)
        initTssClasses(school, adminId)
    else:
        print("园所 ： " + school[1] + "没找到管理员")

cursor.close()
db.commit()
db.close()

print('请输入任意键结束：')
input()
