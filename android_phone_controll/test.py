import os, time

# os.system('adb shell input keyevent 26')
from random import Random

# os.system('adb shell input tap 920 1800')# 进入
# os.system('adb shell input tap 930 993.6 ') 1
# os.system('adb shell input tap 930 1204 ') #2
# os.system('adb shell input tap 930 1504 ') #3
# os.system('adb shell input tap 930 1744 ') #4
# os.system('adb shell input tap 930 2044 ') #6

# os.system('adb shell input tap 594 1545.6  ') # 确认
ss = Random().randint(0, 3)

print(ss)
# os.system('adb shell input keyevent 4')
# for i in range(1,2):
#     print(i)
