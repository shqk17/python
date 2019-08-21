import pymysql, datetime, uuid, time, queue, threading
from time import sleep, ctime
from 补数据专区 import bsUtil, xiancheng

cursor, db = bsUtil.getDBLink(3)

sql = " show tables ; "
cursor.execute(sql)
contents = cursor.fetchall()
selectSql = "select *  from  %s  limit 1 "
selectVersion = "select count(1) as sum from  %s  where version is null;"
if len(contents) < 1:
    print("没有数据")
else:
    for i in contents:
        print(i["Tables_in_tss"])
        cursor.execute(selectSql % (i["Tables_in_tss"]))
        contents1 = cursor.fetchall()
        if len(contents1) < 1:
            continue
        if 'version' in dict(contents1[0]).keys():
            # print(i["Tables_in_tss"] + "--" + "拥有version字段")
            cursor.execute(selectVersion % (i["Tables_in_tss"]))
            contents2 = cursor.fetchall()
            if len(contents2)>0 and int(contents2[0]["sum"]) >0:
                print(i["Tables_in_tss"] + "--" + "有"+str(contents2[0]["sum"]) + "个version字段为空")
cursor.close()
# db.commit()
db.close()

print('请输入任意键结束：')
input()
