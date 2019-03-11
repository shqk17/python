import json, datetime, time

mylist = ["exe", "py"]
s = "exe"
if s in ",".join(mylist):
    print(s)


# flieLog = open("./ces2.txt", "r")
# a = str(flieLog.read())
# print(a)
# s = json.loads(a)
# print(s)
# print("用户" + str(1) + "---断言失败_" + str(datetime.datetime.now()) + "---")
# for j in range(1, 3):
#     print(j)
# timestr = "2019-02-28 16:27:48"
# print(len(timestr))
# day = datetime.datetime.strptime(timestr,'%Y-%m-%d %H:%M:%S')
# st=(day+datetime.timedelta(minutes=-1)).strftime("%Y-%m-%d %H:%M:%S")
# sb=(day+datetime.timedelta(minutes=+1)).strftime("%Y-%m-%d %H:%M:%S")
