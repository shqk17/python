import pymysql, datetime, uuid, time, queue, threading
from time import sleep, ctime
from 补数据专区 import xiancheng
from 菜单同步 import bsUtil

cursor_05, db_05 = bsUtil.getDBLink(2)
cursor_34, db_34 = bsUtil.getDBLink(3)

sql = "select name from sys_dictionary_group"

cursor_05.execute(sql)
contents_05 = cursor_05.fetchall()

cursor_34.execute(sql)
contents_34 = cursor_34.fetchall()

if len(contents_05) < 1 or len(contents_34) < 1:
    print("没有数据")
else:
    tb_05 = []
    for b in contents_05:
        tb_05.append(b["name"])

    tb_05_not = []
    zd_not_in_05 = {}
    for i in contents_34:
        if tb_05.__contains__(i["name"]):
            # 查询当前 分组下 的相值是否缺少
            sql1 = "select id from sys_dictionary_group where name ='" + i["name"] + "' "
            cursor_05.execute(sql1)
            contents_05_zdian_id = cursor_05.fetchall()
            cursor_34.execute(sql1)
            contents_34_zdian_id = cursor_34.fetchall()

            sql2 = "select id,value from sys_dictionary where groupId ='%s'"
            cursor_05.execute(sql2 % contents_05_zdian_id[0]["id"])
            contents_05_zdian = cursor_05.fetchall()
            cursor_34.execute(sql2 % contents_34_zdian_id[0]["id"])
            contents_34_zdian = cursor_34.fetchall()
            if len(contents_05_zdian) != len(contents_34_zdian):
                zd_05 = []
                for i in contents_05_zdian:
                    zd_05.append(i["value"])

                for j in contents_34_zdian:
                    if zd_05.__contains__(j["value"]):
                        pass
                    else:
                        zd_not_in_05[i["id"]] = j
        else:
            tb_05_not.append(i["name"])

    print("新的字典分组：")
    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    getGroupData = "select * from sys_dictionary_group where name = '%s' "
    zd_txt = open("./字典变更sql_"+now_time+".txt", "a")
    zd_txt.write("-- 开始同步字典组*****************************")
    for k in tb_05_not:
        cursor_34.execute(getGroupData % k)
        data = cursor_34.fetchall()[0]
        inset_sql = bsUtil.productSql(data, "sys_dictionary_group")
        zd_txt.write(str(inset_sql))
        print(k)

    print("新增字典项：")
    getZdData = "select * from sys_dictionary where id = '%s' "
    zd_txt.write("-- 开始同步新增字典项*****************************")
    for k, v in zd_not_in_05.items():
        print(str(k) + "---------")
        print(str(v))
        cursor_34.execute(getZdData % v["id"])
        data1 = cursor_34.fetchall()[0]
        inset_sql1 = bsUtil.productSql(data1, "sys_dictionary")
        zd_txt.write(str(inset_sql1))

    zd_txt.close()

cursor_05.close()
# db.commit()
db_05.close()
cursor_34.close()
# db.commit()
db_34.close()

print('请输入任意键结束：')
input()
