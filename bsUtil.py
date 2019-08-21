import pymysql


def getDBLink(type):
    if type == 1:
        db = pymysql.connect(host='192.168.0.34',
                             port=3306,
                             user='root',
                             passwd='Aa12345678',
                             db='tss',
                             charset='utf8'
                             , cursorclass=pymysql.cursors.DictCursor
                             )

    if type == 2:
        db = pymysql.connect(host='hb3-rds20180919.mysql.zhangbei.rds.aliyuncs.com',
                             port=3382,
                             user='qms',
                             passwd='rybu0OsWO2qL7Ef',
                             db='tss',
                             charset='utf8'
                             , cursorclass=pymysql.cursors.DictCursor
                             )
    if type ==3:
        db = pymysql.connect(host='192.168.0.5',
                             port=3306,
                             user='root',
                             passwd='asdfg_qwert@',
                             db='tss',
                             charset='utf8'
                              , cursorclass=pymysql.cursors.DictCursor
                             )

    return db.cursor(), db


def hebing_1(A, B):
    for k, v, in B.items():
        if A.__contains__(k):
            # 做加的操作：
            sss = A[k][2] + v[2]
            A[k] = tuple([A[k][0], A[k][1], sss, A[k][3]])
        else:
            A[k] = v
    return A


def hebing_2(A, B):
    for k, v, in B.items():
        if A.__contains__(k):
            # 做加的操作：
            sss = A[k][2] + v[2]
            mmm = A[k][3] + v[3]
            A[k] = tuple([A[k][0], A[k][1], sss, mmm])
        else:
            A[k] = v
    return A


def suoyin(amap):
    newmap = {}
    for x in amap:
        newmap[str(x[0]) + "-" + str(x[1])] = x
    return newmap


def bijiao2(A, B):
    i = 0
    back = open("./绑定课时包修改前数据备份.txt", encoding="utf-8", mode='a')
    newUpdate = open("./绑定课时包修改后的数据.txt", encoding="utf-8", mode='a')
    for k, v, in B.items():
        if A.__contains__(k):
            # 做加的操作：
            if float('%.2f' % A[k][2]) != float('%.2f' % v[2]) or float('%.2f' % A[k][3]) != float('%.2f' % v[3]):
                print("-------start--------")
                print(A[k])
                back.write(
                    "update tss_member_package_bind set binderPositiveConsumptionClassHour = %s ,binderGiftConsumptionClassHour =%s "
                    " where memberId = '%s' and memberPackageId ='%s' ;\n" % (A[k][2], A[k][3], A[k][0], A[k][1]))
                print(B[k])
                newUpdate.write(
                    "update tss_member_package_bind set binderPositiveConsumptionClassHour = %s ,binderGiftConsumptionClassHour =%s "
                    " where memberId = '%s' and memberPackageId ='%s' ;\n" % (B[k][2], B[k][3], B[k][0], B[k][1]))
                print("-------end--------")
                i = i + 1
    print(i)
    back.close()
    newUpdate.close()


def bijiao2(A, B):
    i = 0
    back = open("./绑定课时包修改剩余未消耗前数据备份.txt", encoding="utf-8", mode='a')
    newUpdate = open("./绑定课时包修改剩余未消耗后的数据.txt", encoding="utf-8", mode='a')
    for k, v, in B.items():
        if A.__contains__(k):
            # 做加的操作：
            if float('%.2f' % A[k][2]) != float('%.2f' % v[2]) or float('%.2f' % A[k][3]) != float('%.2f' % v[3]):
                print("-------start--------")
                print(A[k])
                back.write(
                    "update tss_member_package_bind set binderPositiveUnusedClassHour = %s ,binderGiftUnusedClassHour =%s "
                    " where memberId = '%s' and memberPackageId ='%s' ;\n" % (A[k][2], A[k][3], A[k][0], A[k][1]))
                print(B[k])
                newUpdate.write(
                    "update tss_member_package_bind set binderPositiveUnusedClassHour = %s ,binderGiftUnusedClassHour =%s "
                    " where memberId = '%s' and memberPackageId ='%s' ;\n" % (B[k][2], B[k][3], B[k][0], B[k][1]))
                print("-------end--------")
                i = i + 1
    print(i)
    back.close()
    newUpdate.close()
