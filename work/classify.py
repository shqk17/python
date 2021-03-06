# coding:utf-8
# -*- coding: utf-8 -*-
import os, shutil, datetime

# shutil模块主要是用于拷贝文件

# 取得当前目录下的文件名称列表
files_list = os.listdir()
# 取得python脚本的名字
# __file__是取得当前脚本路径,如果路径是“\anaconda3\python”这样的格式，则要使用“\\”做切分
py_name = __file__.split('/')[-1]
notdoclassify = ["py", "exe"]
for file in files_list:
    print(file)
    # 如果是文件是当前执行的py脚本，则跳过
    if file == py_name:
        print("跳过--1")
        continue
    # 如果当前文件格式不是一个文件如“.”，则跳过
    if not os.path.isfile(file):
        print("跳过--2")
        continue
    # 取得当前文件名称的格式，（切分文件名，取最后的列表元素）
    file_type = file.split('.')[-1]
    if file_type in notdoclassify:
        print("跳过--3")
        continue
    # 如果没有某个格式的文件夹，则创建这个文件夹
    if not os.path.exists(file_type):
        os.mkdir(file_type)
    # 获取当前路径
    path = os.getcwd()
    # 获取分类文件夹路径
    subdir = os.path.join(path, '%s' % file_type)
    # 进入分类文件夹
    os.chdir(subdir)
    if os.path.exists(file):
        # 如果文件夹存在当前文件，则跳过
        print("跳过--4")
        continue
    else:
        # 返回之前文件夹进行归类
        print("执行成功")
        os.chdir(path)
        shutil.move(file, subdir)
