from xlrd import open_workbook
import pymysql

data = open_workbook("111.xlsx")
table1 = data.sheet_by_index(0)
rowNum = table1.nrows
colNum = table1.ncols
if rowNum == 0 or colNum == 0:
    pass
# 获取所有单元格的内容
excelList = []
for i in range(2, rowNum):
    name = table1.cell_value(i, 0);
    contact = table1.cell_value(i, 12);
    suplur = table1.cell_value(i, 22);
    excelList.append(str(name) + "," + str(contact) + "," + str(suplur))
db = pymysql.connect(host='192.168.0.5',
                     port=3306,
                     user='root',
                     passwd='asdfg_qwert@',
                     db='t_tss',
                     charset='utf8'
                     # , cursorclass=pymysql.cursors.DictCursor
                     )
cursor = db.cursor()

sql = "SELECT surplusFormalClassHour from tss_member_package_history a LEFT JOIN tss_student b on a.memberId = b.id LEFT JOIN sys_admin_user c on b.adminUserId = c.id where a.contractNumber='%s'  and c.schoolId='ff80808169a57fe80169b36d5d290241' ORDER BY a.updateTime ASC LIMIT 1;"
error = []
for x in excelList:
    sqlstr = sql % (str(x.split(",")[1].split(".")[0]))
    print("开始查询：" + x.split(",")[0])
    print(sqlstr)
    cursor.execute(sqlstr)
    contents = cursor.fetchall()
    ids = []
    if len(contents) > 0:
        for row in contents:
            if int(row[0]) == int(x.split(",")[2].split(".")[0]):
                print("OK")
            else:
                print("error:___"+x.split(",")[0] + ", " + str(x.split(",")[1].split(".")[0]) + ":" + str(
                    int(row[0])) + "-->excel里：" + str(
                    int(x.split(",")[2].split(".")[0])))
                error.append(x.split(",")[0] + ", " + str(x.split(",")[1].split(".")[0]) + ":" + str(
                    int(row[0])) + "-->excel里：" + str(
                    int(x.split(",")[2].split(".")[0])))
cursor.close()
db.close()
print('查询结束：')
print("一共：" + str(len(error)))
for e in error:
    print(e)
print('请输入任意键结束：')
input()
