# coding:utf-8
import datetime
from time import sleep
import bsUtil, io


def main():
    back = io.open("./报班bug查询并删除.txt", encoding="utf-8", mode='a')
    try:
        sql = "SELECT a.* from tss_member_attend_class_record  a where a.id not in (  " \
              "SELECT attendClassId from tss_member_check_attendance )"
        sql2 = "delete from tss_member_attend_class_record where id ='%s'"
        while True:
            cursor, db = bsUtil.getDBLink(2)
            cursor.execute(sql)
            contents = cursor.fetchall()
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(str(nowTime))
            if len(contents) > 0:
                back.write(str(nowTime) + "--报班发生异常：" + str(len(contents)) + "\n")
                for i in contents:
                    back.write(str(i) + "\n")
                    print(sql2 % i[0])
                    cursor.execute(sql2 % i[0])

            cursor.close()
            db.commit()
            db.close()
            sleep(60)
    except Exception as ee:
        print('添加失败\n')
        print(str(ee) + '\n')
        back.write(str(ee))
        back.close()

if __name__ == '__main__':
    main()
