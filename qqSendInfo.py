from xlrd import open_workbook
from xlutils.copy import copy
import copy
import xlutils
import re
import tkinter as tk
import openpyxl
from openpyxl import load_workbook
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
from tkinter import ttk
import time
import win32gui
import win32con
import win32clipboard as w
def main():
    root = tk.Tk()
    root.title('qq自动消息发送器')
    #第一行
    lbObejct = Label(root, text="请输入QQ聊天对象名称:")
    lbObejct.grid(row=0, column=0)
    pathObejct = StringVar()
    entryObejct = Entry(root, textvariable=pathObejct)
    entryObejct.grid(row=0, column=1, columnspan=3)
    # 第二行
    lbMsg =Label(root, text="请输入自动发送的内容:")
    lbMsg.grid(row=1, column=0)
    pathMsg = StringVar()
    entryMsg = Entry(root, textvariable=pathMsg)
    entryMsg.grid(row=1, column=1, columnspan=3)
    # 第三行
    lbNum = Label(root, text="请输入发送次数:")
    lbNum.grid(row=2, column=0)
    pathNum = StringVar()
    entryNum = Entry(root, textvariable=pathNum)
    entryNum.grid(row=2, column=1, columnspan=3)
    # 第四行
    lbTime = Label(root, text="请输入间隔时间（秒）:")
    lbTime.grid(row=3, column=0)
    pathTime = StringVar()
    entryTime = Entry(root, textvariable=pathTime)
    entryTime.grid(row=3, column=1, columnspan=3)
    # 第五行
    button = Button(root, text="确定", command=lambda: send_qq(entryObejct.get(), entryMsg.get(),entryNum.get(),entryTime.get()))
    button.grid(row=4, column=2)
    root.mainloop()
def getText():
    """获取剪贴板文本"""
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d

def setText(aString):
    """设置剪贴板文本"""
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

def send_qq(to_who, msg,num,diftime):
    """发送qq消息
    to_who：qq消息接收人
    msg：需要发送的消息
    """
    # 获取qq窗口句柄
    qq = win32gui.FindWindow(None, to_who)
    i=0;
    while i<int(num):
        setText(msg)
        # 将消息写到剪贴板
        # 投递剪贴板消息到QQ窗体
        win32gui.SendMessage(qq, 258, 22, 2080193)
        win32gui.SendMessage(qq, 770, 0, 0)
        # 模拟按下回车键
        win32gui.PostMessage(qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 2)  # 向窗口发送 回车键
        win32gui.PostMessage(qq, win32con.WM_KEYUP, win32con.VK_RETURN, 2)
        i=i+1
        time.sleep(float(diftime))

if __name__ == '__main__':
    main()