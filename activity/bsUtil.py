import pymysql


def getDBLink(type):
    if type == 1:
        db = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             passwd='123456',
                             db='ums',
                             charset='utf8'
                             , cursorclass=pymysql.cursors.DictCursor
                             )

    if type == 2:
        db = pymysql.connect(host='rm-8vb1jf512aju12u07fo.mysql.zhangbei.rds.aliyuncs.com',
                             port=3306,
                             user='user_ums',
                             passwd='rJ9dSrO6AMlen1L%#C17@NbD22VGpnt',
                             db='ums',
                             charset='utf8'
                             , cursorclass=pymysql.cursors.DictCursor
                             )
    if type == 3:
        db = pymysql.connect(host='10.51.4.10',
                             port=30999,
                             user='root',
                             passwd='C5BIi0lJiW',
                             db='ums',
                             charset='utf8'
                             , cursorclass=pymysql.cursors.DictCursor
                             )

    return db.cursor(), db


def getDBLinkUms(type):
    if type == 1:
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='123456',
                             db='ums',
                             charset='utf8'
                             , cursorclass=pymysql.cursors.DictCursor
                             )

    if type == 2:
        db = pymysql.connect(host='rm-8vb1jf512aju12u07fo.mysql.zhangbei.rds.aliyuncs.com',
                             port=3306,
                             user='user_ums',
                             passwd='rJ9dSrO6AMlen1L%#C17@NbD22VGpnt',
                             db='ums',
                             charset='utf8'
                             , cursorclass=pymysql.cursors.DictCursor
                             )
    if type == 3:
        db = pymysql.connect(host='10.51.4.10',
                             port=30999,
                             user='root',
                             passwd='C5BIi0lJiW',
                             db='ums',
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
        return None, None


def productSql(data, tb):
    ls = [(k, str(v)) for k, v in data.items() if v is not None]
    sentence = ('INSERT INTO %s (' % tb + ','.join([i[0] for i in ls]) + \
                ') VALUES (' + ','.join(repr(i[1]) for i in ls) + ');\n').replace("'None'", "Null") \
        .replace("\"b\'\\\\x00\'\"", "0").replace("\"b\'\\\\x01\'\"", "1").replace("'0'", "0").replace("'1'", "1")
    # print(sentence)
    return sentence
