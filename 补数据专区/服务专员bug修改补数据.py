import pymysql, datetime, uuid, time, queue, threading
from time import sleep, ctime
from 补数据专区 import bsUtil, xiancheng

cursor, db = bsUtil.getDBLink(2)

sql = "SELECT a.memberId,b.name,a.serviceAdvisorAdminUserId as aSever,b.serviceAdvisorAdminUserId as bSever " \
      "from tss_member_package a LEFT JOIN tss_student b on a.memberId =b.id " \
      "where b.serviceAdvisorAdminUserId is null or b.serviceAdvisorAdminUserId ='null' or " \
      "a.serviceAdvisorAdminUserId ='' or b.serviceAdvisorAdminUserId ='';"
cursor.execute(sql)
contents = cursor.fetchall()
print(len(contents))

cursor.close()
db.close()

print('请输入任意键结束：')
input()
