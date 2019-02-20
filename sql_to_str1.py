import tkinter as tk
import hashlib
import re


def main():
    root = tk.Tk()  # 这里
    # fix the root window size
    # root.minsize(920, 750)
    # root.maxsize(920, 750)  # 这里主要是控制窗口的大小，让窗口大小不能改变
    # root.geometry("1366x250")
    root.title('SQL转换工具')  # 设置主窗口的标题
    # display the quit button
    text = edit(root)  #
    l = tk.Label(root, text='sql工具', fg='white', bg='black', width=100)
    l.grid(row=4,column=0,columnspan=5,sticky=tk.E + tk.W + tk.S + tk.N)
    button(root, text)
    # quitbutton(root)
    root.mainloop()  # 这里进入顶层窗口的循环


# build the edit and result Text，建立两个edit控件


def edit(root):
    edit = tk.Text(root, fg='black', bg='#DCDCDC', font='微软雅黑', width=10, height=15, )
    edit.grid(row=0,column=0,columnspan=5 , sticky=tk.N + tk.E + tk.W)

    # button 传递参数使用lambda函数
    # delete all the value in the text editor
    clear1 = tk.Button(root, text='Clear', width=80, bg='#F5DEB3', font='微软雅黑',
                       command=lambda: edit.delete(1.0, tk.END))


    result = tk.Text(root, fg='black', bg='#DCDCDC', font='微软雅黑', width=30, height=10, )
    result.grid(row=2,column=0,columnspan=5 ,sticky=tk.N + tk.E + tk.W)

    # button 传递参数使用lambda函数
    # delete all the value in the text editor
    clear2 = tk.Button(root, text='Clear', width=80, bg='#F5DEB3', font='微软雅黑',
                       command=lambda: ClearAll(result, edit))
    clear2.grid(row=3,column=0,columnspan=5)
    text = [edit, result]
    return text


# 这里定义窗口中所有的按钮控件，并且显示出来，并且设置好每个按钮的响应函数，使用button的command选项来控制
def button(root, text):
    clu = 0
    transformation = tk.Button(root, text='格式化sql', fg='black',width=20, command=lambda: Transformation(text))
    getSQLField = tk.Button(root, text='获取sql字段', fg='black',width=20, command=lambda: GetSQLField(text))
    sqlFieldToBean = tk.Button(root, text='sql字段转javaBean',width=20, fg='black', command=lambda: SqlFieldToBean(text))
    md5do = tk.Button(root, text='-Md5  Creator-', fg='black',width=20, command=lambda: md5create(text))
    auther = tk.Button(root, text='冯书浩',width=20)
    but = [transformation, md5do, getSQLField, sqlFieldToBean, auther]
    for i in but:
        i.grid(row=1, column=clu, sticky=tk.N + tk.E + tk.W)
        clu += 1
    return but


# 格式化java代码复制的sql 便于美化
def Transformation(text):
    edit, result = text[0], text[1]
    enc = edit.get(1.0, tk.END)
    try:  # .encode('ascii')
        res = strToSql(enc[0:-1])
    except:
        return False
    result.insert(1.0, res)  # .decode('ascii')
    return True


# 格式化java代码复制的sql 便于美化
def strToSql(text):
    s = "".join(str(text).split("\n")).replace("\\n", "").replace("\\t", "").replace("+", "").replace("\"", "").replace(
        "                 ", " ")
    return s


# sql 提取字段转为 逗号拼接字符串
def GetSQLField(text):
    edit, result = text[0], text[1]
    enc = edit.get(1.0, tk.END)
    try:  # .encode('ascii')
        res = strToSql2(enc[0:-1])
    except Exception as e:
        print(e)
        return False
    result.insert(1.0, res)  # .decode('ascii')
    return True


# sql 提取字段转为java bean
def SqlFieldToBean(text):
    edit, result = text[0], text[1]
    enc = edit.get(1.0, tk.END)
    try:  # .encode('ascii')
        res = fieldToBean(enc[0:-1])
    except Exception as e:
        print(e)
        return False
    result.insert(1.0, res)  # .decode('ascii')
    return True


# sql 提取字段转为 逗号拼接字符串
def strToSql2(text):
    s = "".join(str(text).split("\n"))
    aaa = re.split(r'CREATE(.+?)\(', s, 2)
    pattern = re.compile(r'`(.+?)((` varchar)|(` int)|(` date)|(` double)|(` datetime)|(` bit))')
    a = re.findall(pattern, aaa[2])
    field = []
    for i in a:
        field.append(re.findall(r'^[A-Za-z0-9]+$', i[0])[0])
    return ",\n".join(str(i) for i in field)


# sql 提取字段转为java bean
def fieldToBean(text):
    lines = str(text).split("\n")
    aaa = []
    pattern = re.compile(r'`(.+?)((` varchar)|(` int)|(` double)|(` datetime)|(` bit))')
    typePattern = re.compile(r'varchar|int|double|datetime|bit')
    commentPattern = re.compile(r"COMMENT \'(.+?)'")
    titleText = ""
    for l in lines:
        if re.findall(pattern, l):
            if re.findall(commentPattern, l):
                tup = (re.findall(pattern, l)[0][0], re.findall(typePattern, l)[0], re.findall(commentPattern, l)[0])
                aaa.append(tup)
            else:
                tup = (re.findall(pattern, l)[0][0], re.findall(typePattern, l)[0], "")
                aaa.append(tup)
        elif re.findall(r'CREATE TABLE `(.+?)`', l):
            if re.findall(r'`(.+?)`', l):
                titleText = re.findall(r'`(.+?)`', l)[0]

    sss = []
    ssef = []
    for i in aaa:
        # 字段实体
        commentStr = "/**" + i[2] + "**/ \n"
        sss.append(commentStr + operator([i[0], i[1]]))
        # get set方法
        zhujieStr = ""
        if i[0] == "id":
            value = {"value1": titleText, "value2": titleText}
            zhujieStr = "@Id \n@GeneratedValue(generator = \"%(value1)sIDGenerator\", strategy = GenerationType.AUTO)\n" \
                        "@GenericGenerator(name = \"%(value2)sIDGenerator\", strategy = \"uuid\")\n@Column(name = \"id\", nullable = false, length = 32)" \
                        "\npublic String getId() {\n return id;\n } \npublic void setId(String id) {\n this.id = id;\n}" % value
            ssef.append(zhujieStr)
        else:
            zhujieStr = get0perator([i[0], i[1]]) + "\n" + set0perator([i[0], i[1]]) + "\n"
            ssef.append(zhujieStr)
    aText = ";\n".join(sss) + ";\n"
    ssefText = "\n".join(ssef)
    return aText + ssefText


def operator(o):
    dict_oper = {
        'varchar': 'private String ',
        'int': 'private Integer ',
        'double': 'private Double ',
        'datetime': 'private Date ',
        'date': 'private Date ',
        'bit': 'private Boolean '
    }
    return dict_oper.get(o[1]) + o[0]


def get0perator(o):
    getText = "@Column(name = \"%s\", nullable = true)\n" % o[0]
    dict_oper = {
        'varchar': 'public String get',
        'int': 'public Integer get',
        'double': 'public Double get',
        'datetime': 'public Date get',
        'date': 'public Date get',
        'bit': 'public Boolean get'
    }
    return getText + dict_oper.get(o[1]) + (o[0][0].upper() + o[0][1:]) + "(){ return %s; }" % o[0]


def set0perator(o):
    dict_oper = {
        'varchar': 'public void set',
        'int': 'public void set',
        'double': 'public void set',
        'datetime': 'public void set',
        'date': 'public void set',
        'bit': 'public void set'
    }
    oper = {
        'varchar': 'String',
        'int': 'Integer',
        'double': 'Double',
        'datetime': 'Date',
        'date': 'Date',
        'bit': 'Boolean'
    }
    value = {"value1": o[0], "value2": o[0], "value3": o[0]}
    return dict_oper.get(o[1]) + (o[0][0].upper() + o[0][1:]) + "(" + oper.get(
        o[1]) + " %(value1)s ){ this.%(value2)s = %(value3)s ; }" % value


# 这里定义md5生成函数
def md5create(text):
    edit, result = text[0], text[1]
    dec = edit.get(1.0, tk.END)  # 获取edit控件中的内容
    res = hashlib.md5()
    try:
        res.update(dec[0:-1].encode('ascii'))
    except:
        return False
    result.insert(1.0, res.hexdigest())  # 将md5后的数据插入到输出edit控件中
    return True

def ClearAll(result, edit):
    result.delete(1.0, tk.END)
    edit.delete(1.0, tk.END)


if __name__ == '__main__':
    main()
