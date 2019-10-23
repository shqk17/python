import datetime
from time import sleep

from 补数据专区 import bsUtil

sql = "SELECT a.id from tss_member_attend_class_record  a where a.id not in (  " \
      "SELECT attendClassId from tss_member_check_attendance )"
sql2 = "delete from tss_member_attend_class_record where id ='%s'"
while True:
    cursor, db = bsUtil.getDBLink(2)
    cursor.execute(sql)
    contents = cursor.fetchall()
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(str(nowTime))
    if len(contents) > 0:
        back = open("./报班bug查询并删除.txt", encoding="utf-8", mode='a')
        back.write(str(nowTime) + "--报班发生异常：" + str(len(contents)) + "\n")
        for i in contents:
            back.write(str(i) + "\n")
            print(sql2 % i[0])
            cursor.execute(sql2 % i[0])
        back.close()
    cursor.close()
    db.commit()
    db.close()
    sleep(20)
print('请输入任意键结束：')
input()
