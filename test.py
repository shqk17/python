import json, re
from functools import reduce

#
# Get_max_num = lambda s: s > 0
#
# lists = [-1, 0, 2, 1]
# print(str(list(filter(Get_max_num, lists))[0]))
#
# scscs = lambda x, y: x if x > y else y
#
# print(reduce(scscs, lists))
import datetime as datetime

begin_date = datetime.datetime.strptime("2019-09-08 12:00:00", "%Y-%m-%d %H:%M:%S").time()
print(begin_date)

tm = datetime.datetime.strptime("2019-09-08 12:00:00","%Y-%m-%d %H:%M:%S")
time_offset = tm+datetime.timedelta(seconds=1)
print(time_offset.strftime("%Y-%m-%d %H:%M:%S"))
# c = b'\x00'
# string = (ord(b'\x00'))
# print(string)

