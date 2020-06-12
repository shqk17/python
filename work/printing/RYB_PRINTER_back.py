# coding:utf-8
# -*- coding: utf-8 -*-
import traceback, ctypes
import time
import win32api
from tkinter import Scrollbar, RIGHT, LEFT, Listbox, Y, END
import psutil
import win32con
import win32gui_struct
import win32gui
import os
import asyncio
import threading
import datetime
import re
import urllib.parse

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinterInfo, QPrinter
import sys, base64
from PyQt5.QtWidgets import QApplication
import websockets
from appdirs import unicode

Main = None


def print_ts(message):
    return "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message)


# 检测客户端权限，用户名密码通过才能退出循环
class Printer(object):

    @staticmethod
    def getTime():
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return nowTime

    @staticmethod
    def removeHead(text):
        u = "rybprinting://"
        pattern = re.compile(r'rybprinting://')
        if re.findall(pattern, str(text)):
            text = str(text).replace(u, '')
        return text

    def getPrinterList(self):
        printer = []
        printerInfo = QPrinterInfo()
        for item in printerInfo.availablePrinters():
            printer.append(item.printerName())
            self.log.write(Printer.getTime() + "--availablePrinterName --" + str(item.printerName()))
        return str.join(",", printer)

    def getSplitHtml(self):
        pattern = re.compile(r'<html>(.+?)</html>')
        dd = re.findall(pattern, str(self.html))
        return dd

    def getPrinter(self):
        printerInfo = QPrinterInfo()
        for item in printerInfo.availablePrinters():
            print(str(item.printerName()))
            if str(self.p) == str(item.printerName()):
                self.printer = QPrinter(item)
                break

    def printing(self):
        print("进入打印方法")
        try:
            if self.printer is None:
                print("当前打印机未选中")
                return

            print("当前打印机是：" + str(self.printer))
            p = self.printer
            print("获取到doc")
            doc = QTextDocument()
            doc.setDocumentMargin(0)
            self.log.write(Printer.getTime() + "--physicalDpiX --" + str(p.physicalDpiX()) + "\n")
            print('physicalDpiX:' + str(p.physicalDpiX()))
            print('resolution:' + str(p.resolution()))
            self.log.write(Printer.getTime() + "--resolution --" + str(p.resolution()) + "\n")
            print('height:' + str(p.height()))
            self.log.write(Printer.getTime() + "--height --" + str(p.height()) + "\n")
            print('width:' + str(p.width()))
            self.log.write(Printer.getTime() + "--width --" + str(p.width()) + "\n")
            scale = round(p.physicalDpiX() / p.resolution(), 4)
            print('scale:' + str(scale))
            self.log.write(Printer.getTime() + "--scale --" + str(scale) + "\n")
            print('supportedResolutions:' + str(p.supportedResolutions()))
            self.log.write(Printer.getTime() + "--supportedResolutions --" + str(p.supportedResolutions()) + "\n")
            print('logicalDpiX:' + str(p.logicalDpiX()))
            self.log.write(Printer.getTime() + "--logicalDpiX --" + str(p.logicalDpiX()) + "\n")
            doc.setPageSize(
                QSizeF(p.logicalDpiX() * (p.width() / 25.4 / scale),
                       p.logicalDpiY() * (p.height() / 25.4 / scale)))
            splitHitm = self.getSplitHtml()
            for html in splitHitm:
                self.log.write(Printer.getTime() + "--starting print -- \n")
                print("starting print")
                doc.setHtml(html)
                doc.print_(p)
            doc.clear()
            print("ending print")
            self.log.write(Printer.getTime() + "--end print -- \n")
        except Exception as ee:
            print(str(ee))
            self.log.write(Printer.getTime() + "***print - error****" + str(ee) + "\n")
            self.log.close()

    def closeLog(self):
        self.log.close()
        self.app.flush()
        self.app.quit()

    def __init__(self, name, htmls):
        self.app = QApplication(sys.argv)
        self.log = open(
            "./" + datetime.datetime.now().strftime('%Y-%m') + ".log",
            "a")
        self.p = '空'
        self.html = '空'
        self.printer = None
        if len(htmls) > 0:
            self.p = base64.b64decode(urllib.parse.unquote(Printer.removeHead(name))).decode(
                "utf-8")  # 打印机名称
            print("期望调用打印机：" + self.p)
            self.log.write(Printer.getTime() + "--printer --" + self.p + "\n")
            self.html = base64.b64decode(htmls).decode("utf-8")
            print(self.html)
            self.log.write(Printer.getTime() + "--after decode html --" + self.html + "\n")
            self.getPrinter()


class MySocket(object):

    async def check_permit(self, websocket):
        while True:
            recv_str = await websocket.recv()
            print(str(recv_str))
            cred_dict = recv_str.split(";")
            # 密码可以使用 非对称加密 后期完善
            if cred_dict[0] == "admin" and cred_dict[1] == "123456":
                await websocket.send('{"type":"success"}')
                return True
            else:
                response_str = '{"type":"fail"}'
                await websocket.send(response_str)

    async def recv_msg(self, websocket):
        while True:
            try:
                if (websocket._connection_lost) is True:
                    print('另一端断开了连接')
                    break

                recv_text = await websocket.recv()
                if not recv_text:
                    print('另一端断开了连接')
                    continue
                # 或者
                if len(recv_text) == 0:
                    print("另一端断开了连接")
                    continue
                cred_dict = recv_text.split(";")
                print(str(recv_text))
                if (len(cred_dict) == 1 and cred_dict[0] == '1'):
                    # 打印列表
                    printer = Printer('', '')
                    printName = printer.getPrinterList()
                    printer.closeLog()
                    print("printName:" + printName)
                    await websocket.send('{"type":"1","data":"' + str(printName) + '"}')
                elif len(cred_dict) == 3 and cred_dict[0] == '2':
                    # 打印
                    printerName = cred_dict[1]
                    htmlBase64 = cred_dict[2]
                    printer2 = Printer(printerName, htmlBase64)
                    print("调用打印方法")
                    printer2.printing()
                    print("关闭打印方法")
                    printer2.closeLog()
                    await websocket.send('{"type":"打印结束"}')
            except Exception as ee:
                print(str(ee))
                break

    # 服务器端主逻辑
    async def main_logic(self, websocket, path):
        await self.check_permit(websocket)
        await self.recv_msg(websocket)

    def isRunning(self):
        return self.loop.is_running()

    def close(self):
        self.close()

    def restart(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(websockets.serve(self.main_logic, '127.0.0.1', 6893))
        self.loop.run_forever()

    def running(self):
        self.loop.run_until_complete(websockets.serve(self.main_logic, '127.0.0.1', 6893))
        self.loop.run_forever()

    def __init__(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.loop = asyncio.get_event_loop()
        # self.running()
        # t = threading.Thread(target=self.running())  # 创建线程，如果函数里面有参数，args=()
        # t.start()  # 开启线程


class SysTrayIcon(object):
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]
    FIRST_ID = 1314

    def __init__(s,
                 icon,
                 hover_text,
                 menu_options,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name=None, ):
        s.icon = icon
        s.hover_text = hover_text
        s.on_quit = on_quit

        menu_options = menu_options + (('退出', None, s.QUIT),)
        s._next_action_id = s.FIRST_ID
        s.menu_actions_by_id = set()
        s.menu_options = s._add_ids_to_menu_options(list(menu_options))
        s.menu_actions_by_id = dict(s.menu_actions_by_id)
        del s._next_action_id

        s.default_menu_index = (default_menu_index or 0)
        s.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): s.refresh_icon,
                       win32con.WM_DESTROY: s.destroy,
                       win32con.WM_COMMAND: s.command,
                       win32con.WM_USER + 20: s.notify, }
        # 注册窗口类。
        window_class = win32gui.WNDCLASS()
        window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = s.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map  # 也可以指定wndproc.
        s.classAtom = win32gui.RegisterClass(window_class)

    def show_icon(s):
        # 创建窗口。
        hinst = win32gui.GetModuleHandle(None)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        s.hwnd = win32gui.CreateWindow(s.classAtom,
                                       s.window_class_name,
                                       style,
                                       0,
                                       0,
                                       win32con.CW_USEDEFAULT,
                                       win32con.CW_USEDEFAULT,
                                       0,
                                       0,
                                       hinst,
                                       None)
        win32gui.UpdateWindow(s.hwnd)
        s.notify_id = None
        s.refresh_icon()

        win32gui.PumpMessages()

    def show_menu(s):
        menu = win32gui.CreatePopupMenu()
        s.create_menu(menu, s.menu_options)
        # win32gui.SetMenuDefaultItem(menu, 1000, 0)

        pos = win32gui.GetCursorPos()
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        win32gui.SetForegroundWindow(s.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                s.hwnd,
                                None)
        win32gui.PostMessage(s.hwnd, win32con.WM_NULL, 0, 0)

    def destroy(s, hwnd, msg, wparam, lparam):
        if s.on_quit: s.on_quit(s)  # 运行传递的on_quit
        nid = (s.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # 退出托盘图标

    def notify(s, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
            pass  # s.execute_menu_option(s.default_menu_index + s.FIRST_ID)
        elif lparam == win32con.WM_RBUTTONUP:  # 单击右键
            s.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:  # 单击左键
            # pass
            nid = (s.hwnd, 0)
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
            win32gui.PostQuitMessage(0)  # 退出托盘图标
            if Main: Main.root.deiconify()
        return True

    def _add_ids_to_menu_options(s, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in s.SPECIAL_ACTIONS:
                s.menu_actions_by_id.add((s._next_action_id, option_action))
                result.append(menu_option + (s._next_action_id,))
            else:
                result.append((option_text,
                               option_icon,
                               s._add_ids_to_menu_options(option_action),
                               s._next_action_id))
            s._next_action_id += 1
        return result

    def refresh_icon(s, **data):
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(s.icon):  # 尝试找到自定义图标
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       s.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else:  # 找不到图标文件 - 使用默认值
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if s.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD
        s.notify_id = (s.hwnd,
                       0,
                       win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                       win32con.WM_USER + 20,
                       hicon,
                       s.hover_text)
        win32gui.Shell_NotifyIcon(message, s.notify_id)

    def create_menu(s, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = s.prep_menu_icon(option_icon)

            if option_id in s.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                s.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(s, icon):
        # 首先加载图标。
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # 填满背景。
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # "GetSysColorBrush返回缓存的画笔而不是分配新的画笔。"
        #  - 暗示没有DeleteObject
        # 画出图标
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def command(s, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        s.execute_menu_option(id)

    def execute_menu_option(s, id):
        menu_action = s.menu_actions_by_id[id]
        if menu_action == s.QUIT:
            win32gui.DestroyWindow(s.hwnd)
        else:
            menu_action(s)


class _Main:

    def main(s):
        #########################      tkinter界面设定      #####################################
        import tkinter as tk
        window = tk.Tk()
        window.title('RYB打印驱动')
        window.geometry('300x100')
        window.resizable(0, 0)
        # canvas = tk.Canvas(window, width=800, height=900)
        # canvas.pack()
        s.root = window
        # window.mainloop()
        sb = Scrollbar(s.root)
        lb = Listbox(s.root, yscrollcommand=sb.set, width=280)
        sb.pack(side=RIGHT, fill=Y)
        lb.pack(side=LEFT, fill=Y)

        def checkTheard():
            lb.pack(side=LEFT, fill=Y)
            sb.pack(side=RIGHT, fill=Y)
            lb.insert(END, ("-" * 100))
            lb.insert(END, "            驱动程序启动成功，欢迎使用")
            lb.insert(END, ("               请最小化到托盘执行。。。。"))
            lb.insert(END, ("-" * 100))
            socket = MySocket()
            jss = 0
            while True:
                try:
                    jss += 1
                    print("运行中")
                    if socket.isRunning() is True:
                        time.sleep(2)
                    else:
                        socket.restart()
                    # lb.insert(END, "成功1")
                    time.sleep(1)

                except Exception as e:
                    lb.insert(END, e)
                    button = tk.Button(s.root, text='Hit_me', width=20)

        t = threading.Thread(target=checkTheard)  # 创建线程，如果函数里面有参数，args=()
        t.start()  # 开启线程
        sb.config(command=lb.yview)

        ###########################     开始托盘程序嵌入     #####################################

        icons = os.getcwd() + r'\print64.ico'
        print(icons)
        hover_text = "RYB打印驱动"  # 悬浮于图标上方时的提示
        menu_options = ()
        s.sysTrayIcon = SysTrayIcon(icons, hover_text, menu_options, on_quit=s.exit, default_menu_index=1)

        s.root.bind("<Unmap>", lambda event: s.Unmap() if s.root.state() == 'iconic' else False)
        s.root.protocol('WM_DELETE_WINDOW', s.exit)
        s.root.resizable(0, 0)
        s.root.mainloop()

    def switch_icon(s, _sysTrayIcon, icons='E:\python\work\printing\print64.ico'):
        _sysTrayIcon.icon = icons
        _sysTrayIcon.refresh_icon()
        # 点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon

    def Unmap(s):
        s.root.withdraw()
        s.sysTrayIcon.show_icon()

    def exit(s, _sysTrayIcon=None):
        s.root.destroy()
        print('exit...')


def write():
    pid = os.getpid()
    with open('./pid.txt', 'w') as f:
        f.write(str(pid))


def read():
    if os.path.exists('./pid.txt'):
        with open('./pid.txt', 'r')as f:
            pid = f.read()
            return pid
    else:
        return '0'


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if is_admin():
        s = open(
            "./" + datetime.datetime.now().strftime('%Y-%m') + ".log",
            "a")
        try:
            isHaveRunning = False
            pid = int(read())
            if pid:
                running_pids = psutil.pids()
                if pid in running_pids:
                    print('现有其它的runner.py进程执行')
                    isHaveRunning = True
                else:
                    write()
                    print('没有其它的runner.py进程执行')
            else:
                write()
                print('没有其它的runner. py进程执行')

            if isHaveRunning:
                print("程序已启动,不可重复启动")
                s.write(print_ts("程序已启动,不可重复启动"))
                s.close()
            else:
                s.close()
                Main = _Main()
                Main.main()
        except Exception as ee:
            print('添加失败')
            print(str(ee))
            print(str(traceback.format_exc()))
            s.write(str(ee))
            s.write(str(traceback.format_exc()))
            s.close()
    else:
        # 检查python版本 ==3, 是3.0以上版本
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:  # in python2.x
            ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
