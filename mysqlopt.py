import pymysql

db = pymysql.connect(host='192.168.0.5',
                     port=3306,
                     user='root',
                     passwd='asdfg_qwert@',
                     db='tss',
                     charset='utf8', cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()

sql = "SELECT * from tss_member_add_subtract_record " \
      "where memberId ='2c92828665aa68940165b2e014073f3c'and " \
      "tss_member_add_subtract_record.addSubtractType = 2 and " \
      "tss_member_add_subtract_record.classHourType=3 and " \
      "createTime>='2018-12-08 19:31:51'"
data = ('13512345678',)
cursor.execute(sql)
for row in cursor.fetchall():
    print(row)
print('共查找出', cursor.rowcount, '条数据')
cursor.close()
db.close()
