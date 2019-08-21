import pymysql, datetime, uuid, time, queue, threading
from time import sleep, ctime
from 补数据专区 import bsUtil, xiancheng
sql = "SELECT * from tss_member_attend_class_record a where a.createTime is null;"
cursor, db = bsUtil.getDBLink(1)
cursor.execute(sql)
contents = cursor.fetchall()