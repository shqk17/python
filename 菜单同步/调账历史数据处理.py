# -*- coding: gbk -*-
from 菜单同步 import bsUtil
import uuid

bankMap = {
    1: "bankKey2",
    2: "bankKey6",
    3: "bankKey10",
    4: "bankKey2",
}
backCode = 23202007138090
cliamedCode = 2220200734277


def getUUID():
    s_uuid = str(uuid.uuid4())
    l_uuid = s_uuid.split('-')
    return ''.join(l_uuid)


backSqls = []
cliamSqls = []
# 获取所有需要补数据的
allSql = "SELECT * FROM `ums_finance_adjust_recorded` where createTime<='2020-07-15 17:30:00'"
cour, db = bsUtil.getDBLink(2)
cour.execute(allSql)
result = cour.fetchall()
for s in result:
    bankkey = bankMap.get(s["inCompanyType"])
    backToArticleRecorded = {}
    backCode = backCode + 1
    backToArticleRecorded["code"] = backCode
    backToArticleRecorded["payType"] = 1
    backToArticleRecorded["payeeAccount"] = bankkey
    backToArticleRecorded["createtime"] = "2020-07-16 12:00:00"
    backToArticleRecorded["claimstatus"] = 3
    backToArticleRecorded["recheckstatus"] = 3
    backToArticleRecorded["syncstatus"] = 3
    backToArticleRecorded["type"] = 3
    backToArticleRecorded["version"] = 0
    backToArticleRecorded["outerserialnumber"] = getUUID()
    id = getUUID()
    backToArticleRecorded["id"] = id
    backSql = bsUtil.productSql(backToArticleRecorded, "ums_finance_back_to_article_recorded")
    backSqls.append(backSql)
    # 获取认款单数据
    claimSql = "select * from ums_finance_claim where  id = '" + s["claimId"] + "'"
    cour.execute(claimSql)
    claimresult = cour.fetchall()[0]
    financeClaim = {}
    financeClaim["type"] = 3
    financeClaim["version"] = 0
    financeClaim["claimMoney"] = s["adjustMoney"]
    financeClaim["projectname"] = claimresult["programNum"]
    financeClaim["feeName"] = claimresult["feeName"]
    financeClaim["feecode"] = claimresult["code"]
    financeClaim["summoney"] = claimresult["billMoney"]
    financeClaim["configId"] = claimresult["configId"]
    financeClaim["idValue"] = claimresult["idValue"]
    financeClaim["createtime"] = "2020-07-16 12:00:00"
    financeClaim["createadminuserid"] = claimresult["adminUserId"]
    financeClaim["isdelete"] = 0
    financeClaim["outercontractnum"] = claimresult["outerContractNum"]
    financeClaim["projectname"] = claimresult["billUser"]
    financeClaim["backtoarticleid"] = id
    cliamedCode = cliamedCode + 1
    financeClaim["code"] = cliamedCode
    financeClaim["id"] = getUUID()
    financeClaimSql = bsUtil.productSql(financeClaim, "ums_finance_claim_recorded")
    cliamSqls.append(financeClaimSql)
cour.close()
db.close()
for s in backSqls:
    print(s)
print("-------------------------------------------------")
for b in cliamSqls:
    print(b)
