import pymysql


def getDBLink(type):
    if type == 1:
        db = pymysql.connect(host='139.159.205.181',
                             port=3306,
                             user='root',
                             passwd='AA123567',
                             db='mrfz_db',
                             charset='utf8'
                             , cursorclass=pymysql.cursors.DictCursor
                             )



    return db.cursor(), db

