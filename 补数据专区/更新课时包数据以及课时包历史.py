# -*- coding: utf-8 -*-
import uuid
import datetime as datetime
import pymysql
class dateUtils:
    def date_add_seconds(str_time):
        time_old = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        time_offset = time_old + datetime.timedelta(seconds=1)
        return time_offset.strftime("%Y-%m-%d %H:%M:%S")


class bsUtil:
    def getDBLink(type):
        if type == 1:
            db = pymysql.connect(host='192.168.0.34',
                                 port=3306,
                                 user='root',
                                 passwd='Aa12345678',
                                 db='tss',
                                 charset='utf8'
                                 # , cursorclass=pymysql.cursors.DictCursor
                                 )

        if type == 2:
            db = pymysql.connect(host='hb3-rds20180919.mysql.zhangbei.rds.aliyuncs.com',
                                 port=3382,
                                 user='qms',
                                 passwd='rybu0OsWO2qL7Ef',
                                 db='tss',
                                 charset='utf8'
                                 # , cursorclass=pymysql.cursors.DictCursor
                                 )
        if type == 3:
            db = pymysql.connect(host='192.168.0.5',
                                 port=3306,
                                 user='root',
                                 passwd='asdfg_qwert@',
                                 db='tss',
                                 charset='utf8'
                                 # , cursorclass=pymysql.cursors.DictCursor
                                 )

        return db.cursor(), db

    def getZdDBLink(type):
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
        if type == 3:
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

    def inset_history(pakamemId, change, isTh, remark, curor):
        selectPackageHistorySql = "select * from tss_member_package_history where memberPackageId ='%s'order by updateTime desc limit 1"

        curor.execute(selectPackageHistorySql % (pakamemId))
        history = curor.fetchone()
        history['id'] = str(uuid.uuid4()).replace("-", "")
        history['remark'] = remark
        history['updateTime'] = dateUtils.date_add_seconds(str(history['updateTime']))
        history = bsUtil.updateDateStr(change, history, isTh)

        insert_sql = "INSERT INTO tss_member_package_history ( %s ) VALUES ( %s ) "
        name_str = ",".join(dict(history).keys())

        value_str = "','".join(map(lambda x: str(x), dict(history).values()))
        value_str = ("'" + value_str + "'").replace("'None'", "Null") \
            .replace("b'\\x00'", "0").replace("b'\\x01'", "1").replace("'0'", "0").replace("'1'", "1")
        insert_sql = insert_sql % (name_str, value_str)
        print(insert_sql)
        # curor.execute(insert_sql)

    def updateDateStr(change, history, isTh):
        if isTh:
            for k, v in dict(change).items():
                history[k] = v
        else:
            for k, v in dict(change).items():
                if str(v).split(",")[0] == '1':
                    # 加法
                    history[k] = float('%.2f' % float(dict(history).get(k))) + float(
                        '%.2f' % float(str(v).split(",")[1]))
                elif str(v).split(",")[0] == '2':
                    # 减法
                    history[k] = float('%.2f' % float(dict(history).get(k))) - float(
                        '%.2f' % float(str(v).split(",")[1]))
                elif str(v).split(",")[0] == '0':
                    history[k] = float('%.2f' % float(str(v).split(",")[1]))
        return history

    def update_package(pakamemId, change, isTh, remark, curor):
        curor.execute("select  *  from tss_member_package where id = '%s' " % (pakamemId))
        package = curor.fetchone()
        update_sql = "UPDATE  tss_member_package set  %s where id = '%s' "
        zdList = []
        if isTh:
            for k, v in dict(change).items():
                zdList.append(k + "=" + str(v))
        else:
            for k, v in dict(change).items():
                if str(v).split(",")[0] == '1':
                    # 加法
                    newData = float('%.2f' % float(dict(package).get(k))) + float('%.2f' % float(str(v).split(",")[1]))
                    zdList.append(k + "=" + str(newData))
                elif str(v).split(",")[0] == '2':
                    # 减法
                    newData = float('%.2f' % float(dict(package).get(k))) - float('%.2f' % float(str(v).split(",")[1]))
                    zdList.append(k + "=" + str(newData))
                elif str(v).split(",")[0] == '0':
                    zdList.append(k + "=" + str(v))
        updateStr = ",".join(zdList)
        update_sql = update_sql % (updateStr, pakamemId)
        print(update_sql)
        # curor.execute(update_sql)

    # isTh 是否直接替换，否：进行加减
    def updatePackgeDate(pakamemId, memberId, change, isTh, remark):
        curor, zddb = bsUtil.getZdDBLink(2)
        bsUtil.inset_history(pakamemId, change, isTh, remark, curor)
        bsUtil.update_package(pakamemId, change, isTh, remark, curor)
        curor.close()
        # zddb.commit()
        zddb.close()
        return None


if __name__ == '__main__':
    # pakamemId = "2c9215846b892dd6016ba29994f16e41"
    # memberId = "2c9215846b892dd6016ba29994e26e3e"
    pakamemId = input("请输入课时包ID：")
    memberId = input("请输入会员ID：")
    # 是直接替换还是做更新操作
    isTh = False
    isThNum = input("请选择操作类型：1，替换字段；2，加减操作更新字段：")
    print("-----------------------------------------------------")
    isThMs = '您选择的是2：加减课时字段操作\n请输入要变更的字段内容；\n示例: 1：加操作，2：减操作；+ num ：变更的数值\n' \
             '{"unusedClassHour": "1,2", "positiveUnusedClassHour": "1,2",' \
             ' "positiveConsumptionClassHour": "2,2",' \
             '"consumptionClassHour": "2,2",}  '

    if isThNum is not None and isThNum == 1:
        isTh = True
        isThMs = "您选择的是1：替换课时字段操作\n"
    print(isThMs)
    print("-----------------------------------------------------")
    changeTxt = input("请输入您的变更内容：")
    change = eval(changeTxt)
    # 改变 的字段  1 ： 加操作 ，2 ： 减操作+ num :变更的课时数
    # change = {"unusedClassHour": "1,2","positiveUnusedClassHour": "1,2","positiveConsumptionClassHour": "2,2","consumptionClassHour": "2,2"}
    # 历史记录表的备注
    remark =  input('请输入备注：')
    bsUtil.updatePackgeDate(pakamemId, memberId, change, isTh, remark)
    input("请输入任意字符结束任务")
