import pymysql, datetime, uuid, time

db = pymysql.connect(host='hb3-rds20180919.mysql.zhangbei.rds.aliyuncs.com',
                     port=3382,
                     user='qms',
                     passwd='rybu0OsWO2qL7Ef',
                     db='tss',
                     charset='utf8'
                     #, cursorclass=pymysql.cursors.DictCursor
                     )

# db = pymysql.connect(host='192.168.0.5',
#                      port=3306,
#                      user='root',
#                      passwd='asdfg_qwert@',
#                      db='tss',
#                      charset='utf8'
#                      # , cursorclass=pymysql.cursors.DictCursor
#                      )

# db = pymysql.connect(host='127.0.0.1',
#                      port=3306,
#                      user='root',
#                      passwd='aa123567',
#                      db='tss',
#                      charset='utf8'
#                      # , cursorclass=pymysql.cursors.DictCursor
#                      )
cursor = db.cursor()

sql = "SELECT * from (SELECT  a.id,a.stuId,dearSonPackageDiscountSumPrice,classHour," \
      " ( dearSonPresentClassHour + classHour ) AS classHourZy," \
      " dearSonNowUnitPrice," \
      "	 packagePeriodType,a.updateTime," \
      " CASE c.type  WHEN 1 THEN  round ( dearSonPackageDiscountSumPrice / ( dearSonPresentClassHour + classHour ), 2 ) ELSE round ( dearSonPackageDiscountSumPrice / classHour, 2 )" \
      "	 END myjs ,c.type  FROM	tss_payment_approval a  LEFT JOIN tss_student b ON a.stuId = b.id" \
      " LEFT JOIN sys_school c ON b.schoolId = c.id" \
      " WHERE 	packagePeriodType <> 2 AND ( dearSonPresentClassHour + classHour ) != 0 " \
      "AND dearSonNowUnitPrice != '') aa where  aa.dearSonNowUnitPrice !=aa.myjs "

cursor.execute(sql)
contents = cursor.fetchall()

courseIdSql = "update  tss_payment_approval set  dearSonNowUnitPrice = %s  where id ='%s'"
for s in contents:
    print(courseIdSql % (float('%.2f' % s[-2]), s[0]))
    cursor.execute(courseIdSql % (float('%.2f' % s[-2]), s[0]))

cursor.close()
db.commit()
db.close()

print('请输入任意键结束：')
input()
