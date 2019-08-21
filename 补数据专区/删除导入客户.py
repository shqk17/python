import pymysql, datetime, uuid, time, queue, threading
from time import sleep, ctime
from 补数据专区 import bsUtil, xiancheng

sql = "SELECT a.id,b.id from tss_pertain_relation a LEFT JOIN tss_student b on a.studentId =b.id where b.schoolId ='2c92828662fc9804016300925c62069b';"
cursor, db = bsUtil.getDBLink(3)
cursor.execute(sql)
contents = cursor.fetchall()
deleteStr = "DELETE from tss_pertain_relation where id ='%s'"
deleteStr2 = "DELETE from tss_student where id ='%s'"
deleteStr11 = "DELETE from tss_main_relation_base_info where parentId ='%s'"
deleteStr12 = "DELETE from tss_main_relation_customer_relationship where parentId ='%s'"
deleteStr13 = "DELETE from tss_main_relation_hobbies where parentId ='%s'"
deleteStr14 = "DELETE from tss_main_relation_life_style where parentId ='%s'"
deleteStr15 = "DELETE from tss_main_relation_work_background where parentId ='%s'"

for s in contents:
    print("删除了%s" % s[0])
    cursor.execute(deleteStr11 % s[0])
    cursor.execute(deleteStr12 % s[0])
    cursor.execute(deleteStr13 % s[0])
    cursor.execute(deleteStr14 % s[0])
    cursor.execute(deleteStr15 % s[0])
    cursor.execute(deleteStr % s[0])
    cursor.execute(deleteStr2 % s[1])
cursor.close()
db.commit()
db.close()
