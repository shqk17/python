import tkinter as tk
import time
import datetime
import hashlib
from tkinter import *
import pymd5


def sign(userName, password, loginId,pathUrl, result):
    str1 = 'loginId=' + loginId + '&password=' + password + '&userName=' + userName
    timestamp = str(int(time.time()))
    str2 = 'timestamp=' + timestamp + '&' + str1 + '&randomStr=' + 'fysdg234dfg'
    unSignStr = timestamp + str2.lower()[::-1] + 'fysdg234dfg'
    print('unSignStr:'+unSignStr)
    res = hashlib.md5()
    try:
        res.update(unSignStr.encode('ascii'))
    except:
        return False
    signStr = res.hexdigest()
    print(signStr)
    url=pathUrl+'?&loginId=' + loginId + '&password=' + password \
        + '&userName=' + userName+'&sign='+signStr+'&timestamp='+timestamp+'&randomStr=' + 'fysdg234dfg'
    result.insert(1.0, url)
def main():
    root = tk.Tk()
    root.title('红黄蓝接口加密工具')
    lbObejct = Label(root, text="请输入用户名:")
    lbObejct.grid(row=0, column=0)
    pathObejct = StringVar()
    entryObejct = Entry(root, textvariable=pathObejct)
    entryObejct.grid(row=0, column=1, columnspan=3)
    # 第二行
    lbMsg = Label(root, text="请输入密码:")
    lbMsg.grid(row=1, column=0)
    pathMsg = StringVar()
    entryMsg = Entry(root, textvariable=pathMsg)
    entryMsg.grid(row=1, column=1, columnspan=3)
    # 第三行
    lbNum = Label(root, text="请输入loginId:")
    lbNum.grid(row=2, column=0)
    pathNum = StringVar()
    entryNum = Entry(root, textvariable=pathNum)
    entryNum.grid(row=2, column=1, columnspan=3)
    # 第四行
    urlNum = Label(root, text="请输入域名地址:")
    urlNum.grid(row=3, column=0)
    pathUrl = StringVar()
    entryUrl = Entry(root, textvariable=pathUrl)
    entryUrl.grid(row=3, column=1, columnspan=3)
    # 第五行
    result = Text(root, fg='black', bg='#DCDCDC', font='微软雅黑', width=30, height=10, )
    result.grid(row=4, column=0, columnspan=3)
    # 第六行
    button = Button(root, text="确定",
                    command=lambda: sign(entryObejct.get(), entryMsg.get(), entryNum.get(), pathUrl.get(),result))
    button.grid(row=5, column=2)
    root.mainloop()


if __name__ == '__main__':
    main()
