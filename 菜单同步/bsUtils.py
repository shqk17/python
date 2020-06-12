import pymysql


def getDBLink(type):
    if type == 1:
        db = pymysql.connect(host='192.168.0.34',
                             port=3306,
                             user='root',
                             passwd='Aa12345678',
                             db='tss',
                             charset='utf8'
                         #    , cursorclass=pymysql.cursors.DictCursor
                             )

    if type == 2:
        db = pymysql.connect(host='hb3-rds20180919.mysql.zhangbei.rds.aliyuncs.com',
                             port=3382,
                             user='qms',
                             passwd='rybu0OsWO2qL7Ef',
                             db='tss',
                             charset='utf8'
                           #  , cursorclass=pymysql.cursors.DictCursor
                             )
    if type == 3:
        db = pymysql.connect(host='192.168.0.5',
                             port=3306,
                             user='root',
                             passwd='asdfg_qwert@',
                             db='tss',
                             charset='utf8'
                           #  , cursorclass=pymysql.cursors.DictCursor
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
        newmap[str(x["id"])] = x["name"]
    return newmap


def bijiao2(a, b):
    if len(a) == len(b):
        return None, None
    if len(a) > len(b):
        list = []
        for k, v, in a.items():
            if len(b) == 0:
                list.append(k + ',' + v)
            elif b.keys().__contains__(k):
                # 包含了，相同，不处理
                pass
            else:
                list.append(k + ',' + v)
        return list, None
    if len(a) < len(b):
        pass


def productSql(data, tb):
    ls = [(k, str(v)) for k, v in data.items() if v is not None]
    sentence = ('INSERT INTO %s (' % tb + ','.join([i[0] for i in ls]) + \
                ') VALUES (' + ','.join(repr(i[1]) for i in ls) + ');\n').replace("'None'", "Null") \
        .replace("\"b\'\\\\x00\'\"", "0").replace("\"b\'\\\\x01\'\"", "1").replace("'0'", "0").replace("'1'", "1")
    print(sentence)
    return sentence
