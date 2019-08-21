import json, time, datetime, re
from functools import reduce

Get_max_num = lambda s: s > 0

lists = [-1, 0, 2, 1]
print(str(list(filter(Get_max_num, lists))[0]))

scscs = lambda x, y: x if x > y else y

print(reduce(scscs, lists))
