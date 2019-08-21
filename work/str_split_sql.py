import tkinter as tk
import hashlib
import re


def main():
    # file 文件类型的对象
    # 1.txt 的编码方式是 utf-8
    with open('1.txt', 'r', encoding="utf-8") as file:
        x = set()
        for eachLine in file.readlines():
            pattern = re.compile(r'[a-zA-Z\d]{32}')
            if re.findall(pattern, str(eachLine)):
                for i in re.findall(pattern, str(eachLine)):
                    x.add(i)
    newtxt = open('2.txt','w', encoding="utf-8")
    newtxt.write("'"+"','".join(x)+"'")
    newtxt.close()
    file.close()
if __name__ == '__main__':
    main()
