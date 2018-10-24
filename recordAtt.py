import datetime
import tkinter.messagebox
from tkinter import *
txt = open("./kaoqing.txt","a",encoding="utf-8")
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
txt.write("下班时间："+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"\n")
txt.close()
tkinter.messagebox.showinfo("消息提示",'保存成功')