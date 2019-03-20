import tkinter as tk
import time
import hashlib
from tkinter import *


def sign(pathUrl, random, pathParam, result):
    if len(pathParam) == 0:
        return result.insert(1.0, "请输入需要加密的参数")
    Param = str(pathParam).rstrip().split("&")
    if len(Param) == 0:
        return result.insert(1.0, "参数格式不正确")
    Param.sort()
    str1 = "&".join(Param)
    timestamp = str(int(time.time()))
    str2 = 'timestamp=' + timestamp + '&' + str1 + '&randomStr=' + random
    unSignStr = timestamp + str2.lower()[::-1] + random
    print('unSignStr:' + unSignStr)
    res = hashlib.md5()
    try:
        res.update(unSignStr.encode())
    except Exception as e:
        print(e)
        return False
    signStr = res.hexdigest()
    print(signStr)
    url = pathUrl + '?' + str1 + '&sign=' + signStr + '&timestamp=' + timestamp + '&randomStr=' + random
    resulturl = 'unSignStr:' + unSignStr + '\n' + '签名字符串：' + signStr + '\n链接地址：\n' + url
    result.insert(1.0, resulturl)


def main():
    root = tk.Tk()
    root.title('红黄蓝接口加密工具')
    urlNum = Label(root, text="请输入域名地址:", justify=LEFT).pack()
    pathUrl = StringVar()
    entryUrl = Entry(root, textvariable=pathUrl).pack(fill=X)

    lbMsg = Label(root, text="请输入随机字符串:").pack(fill=X)

    pathMsg = StringVar()
    entryMsg = Entry(root, textvariable=pathMsg).pack(fill=X)

    lsParam = Label(root, text="请输入参数串:").pack(fill=X)
    paramMsg = StringVar()
    entryParam = Entry(root, textvariable=paramMsg).pack(fill=X)

    resulttxt = Label(root, text="结果集:").pack(fill=X)
    result = Text(root, fg='black', bg='#DCDCDC', font='微软雅黑', width=50, height=10, ).pack(fill=X)
    # 第六行
    button = Button(root, text="确定", command=lambda: sign(pathUrl.get(), pathMsg.get(), paramMsg.get(), result)).pack(
        fill=X)
    root.mainloop()


if __name__ == '__main__':
    main()
