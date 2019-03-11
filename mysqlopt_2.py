import pymysql, datetime

db = pymysql.connect(host='192.168.0.5',
                     port=3306,
                     user='root',
                     passwd='asdfg_qwert@',
                     db='tss',
                     charset='utf8'
                     , cursorclass=pymysql.cursors.DictCursor
                     )
cursor = db.cursor()

filed = ["presentClassHour",
         "usableTotalClassHour",
         "surplusClassHour",
         "surplusFormalClassHour",
         "surplusPresentClassHour",
         "selectedClassHour",
         "consumptionClassHour",
         "positiveConsumptionClassHour",
         "giftConsumptionClassHour",
         "unusedClassHour",
         "positiveUnusedClassHour",
         "giftUnusedClassHour",
         "remediationClassHour",
         "usableTotal",
         "surplusValidDate",
         "packageTotalClassHour",
         "packageSumPrice",
         "packageOriginalUnitPrice",
         "packageAttendanceDay",
         "packageValidDate",
         "freezeFreeClassHour",
         "freezeRemediationClassHour",
         "nkExpendDay",
         "nkSurplusPresentAttendanceDay",
         "obtainAttendanceDay",
         "positiveObtainAttendanceDay",
         "giftObtainAttendanceDay",
         "sumValidDate",
         "freezeRemediationFormalClassHour",
         "freezeRemediationPresentClassHour",
         "remediationFormalClassHour",
         "remediationPresentClassHour",
         "positiveObtainClassHour",
         "giftObtainClassHour",
         "obtainClassHour"]
sql = "select  %s  " \
      " from tss_member_package_history  where id ='%s' " % (",".join(filed), "2c92828663020e67016339ecdaa026e9")
cursor.execute(sql)
contents = cursor.fetchall()
params = contents[0]
sql2 = "update tss_member_package set "
for i in filed:
    sql2 = sql2 + " " + i + " = " + str(params[i]) + " ,"
sql2 = sql2 + "adminUserId = '%s'  where memberId ='%s' and adminUserId = '%s' ;" % (
"rightAdminUserId", "memberId", "errorAdminUserId")
print(sql2)
