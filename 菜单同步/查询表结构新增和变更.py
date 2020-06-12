import pymysql, datetime, uuid, time, queue, threading
from time import sleep, ctime
from 补数据专区 import bsUtil, xiancheng

cursor_05, db_05 = bsUtil.getDBLink(3)
cursor_34, db_34 = bsUtil.getDBLink(1)

ziduanSql = "select column_name,column_comment,data_type from information_schema.columns where table_name='%s'"

sql = " show tables ; "
cursor_05.execute(sql)
contents_05 = cursor_05.fetchall()

cursor_34.execute(sql)
contents_34 = cursor_34.fetchall()

if len(contents_05) < 1 or len(contents_34) < 1:
    print("没有数据")
else:
    tb_05 = []
    for i in contents_05:
        tb_05.append(i[0])

    tb_05_not = []
    zd_not_in_05 = {}
    for i in contents_34:
        if tb_05.__contains__(i[0]):
            cursor_05.execute(ziduanSql % str(i[0]))
            print(ziduanSql % str(i[0]))
            contents_05_zd = cursor_05.fetchall()
            cursor_34.execute(ziduanSql % str(i[0]))
            contents_34_zd = cursor_34.fetchall()
            if len(contents_05_zd) != len(contents_34_zd):
                # 当前表字段不一致
                zd_05 = []
                for j in contents_05_zd:
                    zd_05.append(j[0])

                not_in_05 = []
                for m in contents_34_zd:
                    if zd_05.__contains__(m[0]):
                        pass
                    else:
                        not_in_05.append(m)
                if len(not_in_05) > 0:
                    zd_not_in_05[str(i[0])] = not_in_05

        else:
            tb_05_not.append(i[0])

    print("新表：")
    for k in tb_05_not:
        print(k)

    print("新增字段：")
    for k,v in zd_not_in_05.items():
        print(str(k)+"---------")
        print(str(v))

cursor_05.close()
# db.commit()
db_05.close()
cursor_34.close()
# db.commit()
db_34.close()

print('请输入任意键结束：')
input()
