import pymysql

db = pymysql.connect(host='192.168.0.5',
                     port=3306,
                     user='root',
                     passwd='asdfg_qwert@',
                     db='tss',
                     charset='utf8'
                     # , cursorclass=pymysql.cursors.DictCursor
                     )
cursor = db.cursor()

tableName = ['tss_member_add_subtract_record',
             'tss_member_attend_class_record',
             'tss_member_check_attendance',
             'tss_member_check_attendance_history',
             'tss_member_follow_up_record',
             'tss_member_package',
             'tss_member_package_attend_class',
             'tss_member_package_history',
             'tss_member_return_class_record'
             ]
sql = "SELECT * from ( SELECT a.id ,a.memberId, a.schoolId as AschoolId,b.schoolId " \
      "from (select a.id,a.memberId,c.schoolId from %s a LEFT JOIN " \
      "tss_student b on a.memberId =b.id LEFT JOIN sys_admin_user c on b.adminUserId =c.id )a " \
      "LEFT JOIN ( select a.id,b.schoolId from %s a LEFT JOIN " \
      "sys_admin_user b on a.adminUserId =b.id ) b on a.id = b.id ) a " \
      "where a.AschoolId != a.schoolId and a.schoolId is not null and  a.schoolId !=''  and a.AschoolId !='';"
schoolMap = {}
for x in tableName:
    try:
        print(sql % (x, x))
        cursor.execute(sql % (x, x))
        contents = cursor.fetchall()
        ids = []
        if len(contents) > 0:
            for row in contents:
                ids.append(row[0])
        schoolMap[x] = ids
    except Exception as e:
        print(e)
for k, v in schoolMap.items():
    print(k + ":" + ",".join(v))

cursor.close()
db.close()
print('请输入任意键结束：')
input()
