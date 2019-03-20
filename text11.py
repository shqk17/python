import time
import hashlib
str1 = 'contact=' + '13051727921' + '&contract=' + 'Q1223' + '&name=' + '总部测试宝宝'
timestamp = str(int(time.time()))
str2 = 'timestamp=' + timestamp + '&' + str1 + '&randomStr=' + 'fysdg234dfg'
unSignStr = timestamp + str2.lower()[::-1] + 'fysdg234dfg'
print('unSignStr:'+unSignStr)
res = hashlib.md5()
try:
    res.update(unSignStr.encode())
except:
    pass
signStr = res.hexdigest()
print("签名:"+signStr)
url='http://127.0.0.1:8081/api/user/collect.do'+'?&contact=' + '13051727921' + '&contract=' + 'Q1223' \
        + '&name=' + '总部测试宝宝'+'&sign='+signStr+'&timestamp='+timestamp+'&randomStr=' + 'fysdg234dfg'
print(url)
