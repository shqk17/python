from 补数据专区 import bsUtil

cursor, db = bsUtil.getDBLink(1)

selectsql = "select id,partTime from sys_admin_user where partTime is not null and partTime!=''"
cursor.execute(selectsql)
result = cursor.fetchall()

updateDate = {}
for i in result:
    print(str(i[0]))
    ss = str(i[1]).split(",")
    dd = []
    for s in ss:
        if s is not None and len(s) > 0:
            dd.append(s)
        else:
            print("空")
    newss = "<" + ">,<".join(dd) + ">"
    updateDate[str(i[0])] = newss
    print(newss)

updatesql = "update sys_admin_user set partTimeTag = '%s' where id ='%s'"

for k, v in updateDate.items():
    cursor.execute(updatesql % (str(v),str(k)))
    # print(updatesql % (str(v), str(k)))

cursor.close()
db.commit()
db.close()