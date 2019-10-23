from 补数据专区 import bsUtil

cursor, db = bsUtil.getDBLink(2)

sql = "SELECT 	aa.id, 	aa.updateTime, 	aa.memberId,	aa.surplusClassHour," \
      "	aa.surplusFormalClassHour,	aa.surplusPresentClassHour,	sum( aa.formalClass ) AS formalClassNum," \
      "	sum( aa.giftClass ) AS giftClassNum FROM	(	SELECT" \
      "		a.*,		b.attendClassId,		b.attendenceStatus,		b.formalClass,		b.giftClass," \
      "b.remedialClass	FROM		( SELECT id, updateTime, memberId, surplusClassHour, surplusFormalClassHour, surplusPresentClassHour FROM tss_member_package WHERE surplusClassHour != ( surplusFormalClassHour + surplusPresentClassHour ) ) a" \
      "	LEFT JOIN tss_member_check_attendance b ON a.memberId = b.memberId	WHERE		b.attendenceStatus = 4" \
      "	AND b.giftClass > 0	) aa " \
      "GROUP BY	aa.memberId"

cursor.execute(sql)
result = cursor.fetchall()
cursor.close()
db.close()
for i in result:
    pakamemId = i[0]
    memberId = i[2]
    isTh = False
    change = {
        "surplusPresentClassHour": "2,"+str(i[-1])
    }
    remark = '考勤退课赠课多还BUG'
    bsUtil.updatePackgeDate(pakamemId, memberId, change, isTh,remark)
