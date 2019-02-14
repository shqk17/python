import pymysql

db = pymysql.connect(host='192.168.0.5',
                     port=3306,
                     user='root',
                     passwd='asdfg_qwert@',
                     db='tss_new',
                     charset='utf8'
                     # , cursorclass=pymysql.cursors.DictCursor
                     )
cursor = db.cursor()

sql = "delete from %s "
set=['sys_school_admin_bind','tss_allocation','tss_app_activity','tss_app_appointment_manage','tss_app_follow_up_record',
     'tss_app_member_attend_class_record','']
cursor.execute(sql)
i = 1
for row in cursor.fetchall():
    print(row[0])
    sql2 = "delete from tss_member_return_premium_history where id = '%s'" % (row[0])
    print(sql2)
    cursor.execute(sql2)
    i = i + 1
db.commit()
print('共查找出', i, '条数据')
cursor.close()
db.close()
print('请输入任意键结束：')
input()
