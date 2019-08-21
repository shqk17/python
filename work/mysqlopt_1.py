import pymysql, datetime

db = pymysql.connect(host='192.168.0.5',
                     port=3306,
                     user='root',
                     passwd='asdfg_qwert@',
                     db='tss',
                     charset='utf8'
                     # , cursorclass=pymysql.cursors.DictCursor
                     )
cursor = db.cursor()

countSql = "SELECT count(a.id) as num from tss_right_statistic_monthly_report_task_record a LEFT JOIN tss_student b on a.memberId =b.id LEFT JOIN sys_school c on b.schoolId= c.id WHERE c.type BETWEEN 2 and 3 "
sql = "SELECT a.id from tss_right_statistic_monthly_report_task_record a LEFT JOIN tss_student b on a.memberId =b.id LEFT JOIN sys_school c on b.schoolId= c.id WHERE c.type !=1 limit 1000"
deleteSql = "delete from tss_right_statistic_monthly_report_task_record where id in (%s)"
cursor.execute(countSql)
contents = cursor.fetchall()
allNum = contents[0][0]
print(str(allNum))
while allNum > 0:
    cursor.execute(sql)
    contents1 = cursor.fetchall()
    idlist = []
    for i in contents1:
        idlist.append(i[0])
    ids = "'"+"','".join(idlist) +"'"
    print(ids)
    cursor.execute(deleteSql % ids)
    allNum -= 1000
    idlist.clear()
    print(str(allNum))
cursor.close()
db.commit()
db.close()
print('请输入任意键结束：')
input()
