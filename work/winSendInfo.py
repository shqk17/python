import win32api

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
    # 第一行
    lbObejct = Label(root, text="请输入QQ聊天对象名称:")
    lbObejct.grid(row=0, column=0)
    pathObejct = StringVar()
    entryObejct = Entry(root, textvariable=pathObejct)
    entryObejct.grid(row=0, column=1, columnspan=3)
    # 第二行
    lbMsg = Label(root, text="请输入自动发送的内容:")
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
    button = Button(root, text="确定",
                    command=lambda: send(entryObejct.get(), entryMsg.get(), pathObejct, entryNum.get(), entryTime.get()))
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


def ctrlV():
    win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
    win32api.keybd_event(86, 0, 0, 0)  # v键位码是86
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


def altS():
    win32api.keybd_event(18, 0, 0, 0)  # Alt
    win32api.keybd_event(83, 0, 0, 0)  # s
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)

def send(to_who, msg, pathMsg, num, diftime):
    pathMsg.set("请输入名称")

    tid = win32gui.FindWindow(None, to_who)
    # left, top, right, bottom = win32gui.GetWindowRect(tid)
    i = 0;
    while i < int(num):
        setText(msg)
        ctrlV()
        altS()
        i = i + 1
        time.sleep(float(diftime))


if __name__ == '__main__':
    main()
