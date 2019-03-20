import pymysql, datetime

db = pymysql.connect(host='192.168.0.5',
                     port=3306,
                     user='root',
                     passwd='asdfg_qwert@',
                     db='tss',
                     charset='utf8'
                     , cursorclass=pymysql.cursors.DictCursor
                     )
cursor = db.cursor()

checkstudent = ["2c92828663d8647a0163ee98c83f180f"]
sql = ""

attendMap = []


def actionCompera(action, atend, history):
    # 动作对应 unusedClassHour，selectedClassHour 加减规则 0 不变，1 加，2减
    action_map = {"00", "0,0",
                  "11", "0,0",
                  "22", "0,0",
                  "33", "0,0",
                  "01", "2,0",
                  "02", "2,2",
                  "03", "2,0",
                  "12", "0,2",
                  "13", "0,0",
                  "21", "0,1",
                  "23", "0,1",
                  "31", "0,0",
                  "32", "0,2",
                  }
    packagehistorysql =""

def check_attendence(x):
    sql = "select * from tss_member_check_attendance_history " \
          "	where  memberId='%s' and isDelete=0  " \
          "	  order by updateTime asc"
    print(sql % (x))
    cursor.execute(sql % (x))
    contents = cursor.fetchall()
    everyAttend = {}
    if len(contents) > 0:
        for row in contents:
            attendMap.append(row)
    for atend in attendMap:
        s = atend.get("attendClassId")
        if everyAttend.get(s):
            # 证明有历史数据
            history = everyAttend.get(s)  # 本次atend和历史history进行比较
            print(history)
            print(atend)
            print("-----------------------------------------")
            now_action = atend["attendenceStatus"]
            old_action = history["attendenceStatus"]
            actionCompera(now_action + old_action, atend, history)
            # 做完比较把历史冲掉
            everyAttend[s] = atend
        else:
            everyAttend[s] = atend


for x in checkstudent:
    try:
        check_attendence(x)
    except Exception as e:
        print(e)

cursor.close()
db.close()
print('请输入任意键结束：')
input()
