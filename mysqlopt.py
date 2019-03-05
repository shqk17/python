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

sql = "SELECT " \
      "a.id," \
      "a.schoolName," \
      "group_concat(b.id SEPARATOR \"','\") AS ids," \
      "group_concat(b.realName SEPARATOR \"','\") AS NAMES " \
      "FROM " \
      "sys_school a " \
      "LEFT JOIN sys_admin_user b ON a.id = b.schoolId " \
      "GROUP BY a.id"

print(sql)
cursor.execute(sql)
contents = cursor.fetchall()
schoolMap = {}
i = 1
for row in contents:
    print(1111)
    print(row)
    schoolMap[row[0]] = row[2]
    i = i + 1
print('共查找出', i, '条数据')
sql2 = "SELECT " \
       "a.id,a.memberId,a.adminUserId,c.schoolId " \
       "FROM " \
       "tss_member_package a  " \
       "LEFT JOIN  tss_student b on a.memberId=b.id " \
       "LEFT JOIN  sys_admin_user c on b.adminUserId=c.id"
cursor.execute(sql2)
contents2 = cursor.fetchall()
memberP = []
for row2 in contents2:
    memberP.append(row2[0]+ "," + row2[1] + "," + row2[2] + "," + row2[3])
inList = []
notInList = []
for k in memberP:
    try:
        if len(schoolMap[k.split(",")[3]]) > 0:
            if k.split(",")[2] in schoolMap[k.split(",")[3]]:
                inList.append(k)
            else:
                notInList.append(k)
    except Exception as e:
        pass

print("END--------:")
for l in notInList:
    print(l)

cursor.close()
db.close()
print('请输入任意键结束：')
input()
