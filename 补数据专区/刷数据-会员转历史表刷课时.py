from 补数据专区 import bsUtil
import re

cursor, db = bsUtil.getDBLink(1)

selectsql = "select id,HandleContent from tss_member_turn_history_record where handleMatter =1"
cursor.execute(selectsql)
result = cursor.fetchall()

updateSql = "update tss_member_turn_history_record set formalClass =%s ,giftClass=%s ," \
            " remedialClass=%s where id = '%s'"
for i in result:
    formal = 0.0
    formalS = re.findall(r'正课:(.*?)课时', i[1])
    if formalS is not None and len(formalS) > 0:
        formal = formal + float('%.2f' % float(formalS[0]))
    giftS = re.findall(r';转已消耗增课:(.*?)课时', i[1])

    gift = 0.0
    if giftS is not None and len(giftS) > 0:
        gift = gift + float('%.2f' % float(giftS[0]))
    remedialClass_one = re.findall(r'补课课时:(.*?)$', i[1])
    remedialClass = 0.0
    if remedialClass_one is not None and len(remedialClass_one) > 0:
        remedialClass = remedialClass + float('%.2f' % float(remedialClass_one[0]))
    remedialClass_two = re.findall(r'补课转已消耗增课:(.*?)课时', i[1])
    if remedialClass_two is not None and len(remedialClass_two) > 0:
        remedialClass = remedialClass + float('%.2f' % float(remedialClass_two[0]))
    print(str(updateSql % (formal, gift, remedialClass, i[0])))
    cursor.execute(updateSql % (formal, gift, remedialClass, i[0]))
    print("-正：%s-赠:%s-补:%s-" % (formal, gift, remedialClass))

cursor.close()
db.commit()
db.close()
