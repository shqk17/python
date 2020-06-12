# from tkinter import Tk
# from tkinter.messagebox import askyesno
#
# def closeWindow():
#     ans = askyesno(title='Warning',message='Close the window?')
#     if ans:
#         root.destroy()
#     else:
#         return
#
# if __name__ == '__main__':
#     root = Tk()
#     root.protocol('WM_DELETE_WINDOW', closeWindow)
#     root.mainloop()
import tkinter as tk

root= tk.Tk()

root.title("wm min/max")

# this removes the maximize button
root.resizable(0,0)

# # if on MS Windows, this might do the trick,
# # but I wouldn't know:
# root.attributes(toolwindow=1)

# # for no window manager decorations at all:
# root.overrideredirect(1)
# # useful for something like a splash screen
root.mainloop()