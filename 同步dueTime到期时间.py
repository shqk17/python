from 补数据专区 import bsUtil
import datetime

sql = "SELECT dueTime,userUeffectiveEndTime,ueffectiveEndTime,id " \
      " from tss_member_package where " \
      " schoolId ='2c92828569e2df69016a118f2ac8003d' and " \
      " (dueTime<userUeffectiveEndTime or dueTime<ueffectiveEndTime)"

updateSql = "update tss_member_package set dueTime ='%s' , ueffectiveEndTime='%s' , surplusValidDate='%s' where id = '%s';"
cursor, db = bsUtil.getDBLink(1)

sqllist = []

cursor.execute(sql)
context = cursor.fetchall()


def getDateDiff(time):
    nowTime = datetime.datetime.now()
    dateTime_p = datetime.datetime.strptime(str(time), '%Y-%m-%d')
    diffday = str(int((dateTime_p - nowTime).days) + 1)
    print(diffday)
    if int((dateTime_p - nowTime).days) + 1 < 1:
        return "0"
    return diffday


if len(context) < 1:
    print("无数据")
else:
    for i in context:
        sqllist.append(updateSql % (i[1], i[1], getDateDiff(i[1]), i[3]))


for s in sqllist:
    print(s)

db.close()