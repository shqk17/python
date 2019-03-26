from hashlib import sha1
import time
# 需要加密的字符串
pwd = "2c9282866402cd550164179e05ab7bb6"
time_str = '2018-06-19 18:36:29'
# 转为时间数组，分别利用time模块和datetime模块
timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
password = 'qzy123456'
timeStamp = int(time.mktime(timeArray))

pwd = pwd + password + str(timeStamp)
# 创建sha1对象
s1 = sha1()
# 对s1进行更新
s1.update(pwd.encode())
# 加密处理
result = s1.hexdigest()
# 结果是40位字符串：'40bd001563085fc35165329ea1ff5c5ecbdbbeef'
print(result)