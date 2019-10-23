from 补数据专区 import bsUtil

cursor, db = bsUtil.getDBLink(2)

pakamemId = "2c9282876d496ec9016d4cbcea685154"
memberId = "2c9282876d496ec9016d4cbcea545151"

pakamemId1 = "2c92828664a339f60164dfe55d906c6b"
memberId1 = "2c92828664a339f60164dfe55d816c68"
isTh = False
change = {
    "unusedClassHour": "1,"+"1",
    "positiveConsumptionClassHour": "2,"+"1",
    "consumptionClassHour": "2,"+"1",
}
remark = '会员批量出勤重复点击'
bsUtil.updatePackgeDate(pakamemId, memberId, change, isTh,remark)
bsUtil.updatePackgeDate(pakamemId1, memberId1, change, isTh,remark)
