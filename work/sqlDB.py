import pymysql, datetime,uuid
db = pymysql.connect(host='hb3-rds20180919.mysql.zhangbei.rds.aliyuncs.com',
                     port=3382,
                     user='qms',
                     passwd='rybu0OsWO2qL7Ef',
                     db='tss',
                     charset='utf8'
                     #, cursorclass=pymysql.cursors.DictCursor
                     )
cursor = db.cursor()


getTxsql = "SELECT DISTINCT b.id as id  from tss_course a LEFT JOIN sys_admin_user b on a.adminUserId =B.id where b.post=1 GROUP BY b.schoolId";
cursor.execute(getTxsql)
contents = cursor.fetchall()
insertSql1 = "INSERT INTO `tss_course`(`id`, `systemId`, `systemPid`, `adminUserId`, `type`, `status`, `createTime`, `updateTime`, `version`, `isBlockUp`, `trialAge`, `trialAgeStart`, `trialAgeEnd`) VALUES ('%s', '64de5628532f4c81be791af57bb94d51', '7d0960cf77494c52b3d8b5eaef1b3ba6', '%s', 1, NULL, '2019-06-17 09:25:12', '2019-06-17 09:25:12', 1, b'0', NULL, NULL, NULL);"
insertSql2 = "INSERT INTO `tss_course`(`id`, `systemId`, `systemPid`, `adminUserId`, `type`, `status`, `createTime`, `updateTime`, `version`, `isBlockUp`, `trialAge`, `trialAgeStart`, `trialAgeEnd`) VALUES ('%s', 'b95bf9e645f448c08da26599790f0933', '7d0960cf77494c52b3d8b5eaef1b3ba6', '%s', 1, NULL, '2019-06-17 09:25:12', '2019-06-17 09:25:12', 1, b'0', NULL, NULL, NULL);"
insertSql3 = "INSERT INTO `tss_course`(`id`, `systemId`, `systemPid`, `adminUserId`, `type`, `status`, `createTime`, `updateTime`, `version`, `isBlockUp`, `trialAge`, `trialAgeStart`, `trialAgeEnd`) VALUES ('%s', 'dab40fde3d7f4a339861e6dd7b1b16d0', '7d0960cf77494c52b3d8b5eaef1b3ba6', '%s', 1, NULL, '2019-06-17 09:25:12', '2019-06-17 09:25:12', 1, b'0', NULL, NULL, NULL);"
insertSql4 = "INSERT INTO `tss_course`(`id`, `systemId`, `systemPid`, `adminUserId`, `type`, `status`, `createTime`, `updateTime`, `version`, `isBlockUp`, `trialAge`, `trialAgeStart`, `trialAgeEnd`) VALUES ('%s', '15c1e7d75f484a39a43216c1722b3a1c', '7d0960cf77494c52b3d8b5eaef1b3ba6', '%s', 1, NULL, '2019-06-17 09:25:12', '2019-06-17 09:25:12', 1, b'0', NULL, NULL, NULL);"
if len(contents) > 0:
    num = 0
    for s in contents:
        print(insertSql1 %("".join(str(uuid.uuid4()).split("-")),s[0]));
        print(insertSql2 %("".join(str(uuid.uuid4()).split("-")),s[0]));
        print(insertSql3 %("".join(str(uuid.uuid4()).split("-")),s[0]));
        print(insertSql4 %("".join(str(uuid.uuid4()).split("-")),s[0]));
        cursor.execute(insertSql1 %("".join(str(uuid.uuid4()).split("-")),s[0]));
        cursor.execute(insertSql2 %("".join(str(uuid.uuid4()).split("-")),s[0]));
        cursor.execute(insertSql3 %("".join(str(uuid.uuid4()).split("-")),s[0]));
        cursor.execute(insertSql4 %("".join(str(uuid.uuid4()).split("-")),s[0]));
        num +=4
    print("一共有---"+str(num))
cursor.close()
db.commit()
db.close()
print('请输入任意键结束：')
input()


#获取所有的课程体系；
# sql = "select id,name from sys_course_system where pId is null or pId =''"
# cursor.execute(sql)
# contents = cursor.fetchall()
# kcTX = {}
# if len(contents) > 0:
#     kcTX = contents