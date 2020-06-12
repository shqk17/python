# coding:utf-8
# -*- coding: utf-8 -*-
import asyncio
import base64
import datetime
import os
import re
import subprocess
import sys
import threading
import time
import urllib.parse
from tkinter import Scrollbar, RIGHT, LEFT, Listbox, Y, END
from tkinter.messagebox import askyesno

import websockets
import win32api
import win32con
import win32gui
import win32gui_struct
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinterInfo, QPrinter
from PyQt5.QtWidgets import QApplication

Main = None


def print_ts(message):
    return "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message)

def logprint(msg):
    logger = open(
        "./" + datetime.datetime.now().strftime('%Y-%m') + ".log",
        "a", encoding="utf-8")
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.write(nowTime + "--main --" + str(msg) + "--\n")
    logger.flush()
    logger.close()

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
            logprint("--availablePrinterName --" + str(item.printerName()))
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
        logger = open(
            "./" + datetime.datetime.now().strftime('%Y-%m') + "main.log",
            "a", encoding="utf-8")
        logger.write(Printer.getTime() + "--进入打印方法 --\n")
        try:
            if self.printer is None:
                logger.write(Printer.getTime() + "--当前打印机未选中 --\n")
                return

            print("当前打印机是：" + str(self.printer))
            logger.write(Printer.getTime() + "--当前打印机是："+str(self.printer)+" --\n")
            p = self.printer
            print("获取到doc")
            logger.write(Printer.getTime() + "--获取到doc --\n")
            doc = QTextDocument()
            doc.setDocumentMargin(0)
            logger.write(Printer.getTime() + "--physicalDpiX --" + str(p.physicalDpiX()) + "\n")
            print('physicalDpiX:' + str(p.physicalDpiX()))
            print('resolution:' + str(p.resolution()))
            logger.write(Printer.getTime() + "--resolution --" + str(p.resolution()) + "\n")
            print('height:' + str(p.height()))
            logger.write(Printer.getTime() + "--height --" + str(p.height()) + "\n")
            print('width:' + str(p.width()))
            logger.write(Printer.getTime() + "--width --" + str(p.width()) + "\n")
            scale = round(p.physicalDpiX() / p.resolution(), 4)
            pwscale = round(p.logicalDpiX() / 96, 2)
            xyScale = round(float(str(p.height())) / float(str(p.width())), 2)
            print('scale:' + str(scale))
            print('pwscale:' + str(pwscale))
            print('xyScale:' + str(xyScale))
            logger.write(Printer.getTime() + "--scale --" + str(scale) + "\n")
            logger.write(Printer.getTime() + "--pwscale --" + str(pwscale) + "\n")
            logger.write(Printer.getTime() + "--xyScale --" + str(xyScale) + "\n")
            print('supportedResolutions:' + str(p.supportedResolutions()))
            logger.write(Printer.getTime() + "--supportedResolutions --" + str(p.supportedResolutions()) + "\n")
            print('logicalDpiX:' + str(p.logicalDpiX()))
            print('logicalDpiY:' + str(p.logicalDpiY()))
            logger.write(Printer.getTime() + "--logicalDpiX --" + str(p.logicalDpiX()) + "\n")
            logger.write(Printer.getTime() + "--logicalDpiY --" + str(p.logicalDpiY()) + "\n")
            print('xsize:' + str(p.logicalDpiX() * (p.width() / 25.4 / scale) / pwscale))
            logger.write(
                Printer.getTime() + "--xsize --" + str(p.logicalDpiX() * (p.width() / 25.4 / scale) / pwscale) + "\n")
            xsize = p.logicalDpiX() * (p.width() / 25.4 / scale) / pwscale / pwscale
            logger.write(Printer.getTime() + "--xsize --" + str(xsize) + "\n")
            ysize = xsize * xyScale
            logger.write(Printer.getTime() + "--ysize --" + str(ysize) + "\n")
            doc.setPageSize(
                QSizeF(xsize, ysize))
            splitHitm = self.getSplitHtml()
            for html in splitHitm:
                logger.write(Printer.getTime() + "--starting print -- \n")
                print("starting print")
                doc.setHtml(html)
                doc.print_(p)
            doc.clear()
            print("ending print")
            logger.write(Printer.getTime() + "--end print -- \n")
        except Exception as ee:
            print(str(ee))
            logger.write(Printer.getTime() + "***print - error****" + str(ee) + "\n")
            logger.close()
        logger.close()

    def closeLog(self):
        self.app.flush()
        self.app.quit()

    def __init__(self, name, htmls):
        self.app = QApplication(sys.argv)
        log = open(
            "./" + datetime.datetime.now().strftime('%Y-%m') + ".log",
            "a")
        self.p = '空'
        self.html = '空'
        self.printer = None
        if len(htmls) > 0:
            self.p = base64.b64decode(urllib.parse.unquote(Printer.removeHead(name))).decode(
                "utf-8")  # 打印机名称
            print("期望调用打印机：" + self.p)
            log.write(Printer.getTime() + "--printer --" + self.p + "\n")
            self.html = base64.b64decode(htmls).decode("utf-8")
            print(self.html)
            log.write(Printer.getTime() + "--after decode html --" + self.html + "\n")
            self.getPrinter()
        log.close()

class MySocket(object):



    async def check_permit(self, websocket):
        while True:
            recv_str = await websocket.recv()
            logprint("通信1："+str(recv_str))
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
                if websocket is None:
                    logprint('另一端断开了连接')
                    break

                recv_text = await websocket.recv()
                if not recv_text:
                    logprint('另一端断开了连接')
                    break
                # 或者
                if len(recv_text) == 0:
                    logprint('另一端断开了连接')
                    break

                cred_dict = recv_text.split(";")
                print("通信2：" +str(recv_text))
                logprint("通信2：" + str(recv_text))
                if (len(cred_dict) == 1 and cred_dict[0] == '1'):
                    # 打印列表
                    printer = Printer('', '')
                    printName = printer.getPrinterList()
                    printer.closeLog()
                    logprint("printName:" + printName)
                    await websocket.send('{"type":"1","data":"' + str(printName) + '"}')
                elif len(cred_dict) == 3 and cred_dict[0] == '2':
                    # 打印
                    printerName = cred_dict[1]
                    htmlBase64 = cred_dict[2]
                    printer2 = Printer(printerName, htmlBase64)
                    print("调用打印方法")
                    logprint("调用打印方法")
                    printer2.printing()
                    logprint("关闭打印方法")
                    printer2.closeLog()
                    await websocket.send('{"type":"打印结束"}')

            except Exception as ee:
                logprint("通信2：" +str(ee))
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
        s.logprint("程序启动")
        window = tk.Tk()
        window.title('RYB打印驱动')
        window.geometry('300x100')
        window.resizable(0, 0)

        s.root = window
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
                    if socket.isRunning() is True:
                        print("运行中")
                        time.sleep(2)
                    else:
                        print("重启中")
                        socket.restart()
                    print(jss)
                    s.logprint('任务执行计数器'+str(jss))
                    time.sleep(0.5)
                except Exception as e:
                    if str(e.args[0]) == '10048':
                        print("请勿重复启动")
                        s.logprint("请勿重复启动")
                        s.root.destroy()
                    else:
                        print(str(e))
                        s.logprint(str(e))
                        s.root.destroy()

        t = threading.Thread(target=checkTheard)  # 创建线程，如果函数里面有参数，args=()
        t.start()  # 开启线程
        sb.config(command=lb.yview)

        ###########################     开始托盘程序嵌入     #####################################

        icons = os.getcwd() + r'\print64.ico'
        print("---------------icons-------------------" + str(icons))
        hover_text = "RYB打印驱动"  # 悬浮于图标上方时的提示
        menu_options = ()
        s.sysTrayIcon = SysTrayIcon(icons, hover_text, menu_options, on_quit=s.exited, default_menu_index=1)

        s.root.bind("<Unmap>", lambda event: s.Unmap() if s.root.state() == 'iconic' else False)
        s.root.protocol('WM_DELETE_WINDOW', s.exit)
        s.root.resizable(0, 0)
        s.root.mainloop()

    def switch_icon(s, _sysTrayIcon, icons='E:\python\work\printing\print64.ico'):
        _sysTrayIcon.icon = icons
        _sysTrayIcon.refresh_icon()
        # 点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon

    # 最小化
    def Unmap(s):
        s.root.withdraw()
        s.sysTrayIcon.show_icon()

    def killProssece(s):
        logprint("退出程序--删除进程")
        try:
            subprocess.run('taskkill /f /fi "IMAGENAME eq RYB打印驱动.exe"', shell=True)
        except Exception as e:
            logprint("退出程序异常")
            logprint(str(e))

    def exited(s, _sysTrayIcon=None):
        ans = askyesno(title='Warning', message='是否确认退出？退出后将不能使用热敏打印功能')
        if ans:
            t = threading.Thread(target=s.killProssece)  # 创建线程，如果函数里面有参数，args=()
            t.start()  # 开启线程
            s.root.destroy()
            sys.exit(0)
            logprint("退出窗口")
            print('exit...')

    def exit(s, _sysTrayIcon=None):
        # 把关闭窗口重写为最小化
        s.Unmap()

    def logprint(s, msg):
        logger = open(
            "./" + datetime.datetime.now().strftime('%Y-%m') + "main.log",
            "a", encoding="utf-8")
        logger.write(Printer.getTime() + "--" + str(msg) + "--\n")
        logger.flush()
        logger.close()


if __name__ == '__main__':
    Main = _Main()
    Main.main()
