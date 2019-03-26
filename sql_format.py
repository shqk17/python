import sys, time, hashlib
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import requests
import json, re
from sql_format_form import Ui_MainWindow


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("sql_format")
        # 格式化sql
        self.pushButton_1.clicked.connect(self.strToSql)
        # x,x->x','x
        self.pushButton_2.clicked.connect(self.dhChongzu)
        # 获取sql字段
        self.pushButton_3.clicked.connect(self.GetSQLField)
        # sql转javabean
        self.pushButton_4.clicked.connect(self.SqlFieldToBean)
        # mybatis mapper to sql
        self.pushButton_5.clicked.connect(self.mapperToSql)
        # sql to pythonType
        self.pushButton_6.clicked.connect(self.topysql)
        # xx->xx,
        self.pushButton_7.clicked.connect(self.idFormat)

        # 清空按钮
        self.pushButton_11.clicked.connect(self.clearAll)

    def clearAll(self):
        self.textEdit.clear()
        self.resultEdit.clear()

    def strToSql(self):
        try:
            text = self.textEdit.toPlainText()
            s = "".join(str(text).split("\n")).replace("\\n", "").replace("\\t", "").replace("+", "").replace("\"",
                                                                                                              "").replace(
                "                 ", " ")
            self.resultEdit.clear()
            self.resultEdit.insertPlainText(s)
        except:
            self.resultEdit.clear()
            self.resultEdit.insertPlainText("格式错误，请重试")

    def dhChongzu(self):
        try:
            text = self.textEdit.toPlainText()
            s = "','".join(text.split(","))
            self.resultEdit.clear()
            self.resultEdit.insertPlainText(s)
        except:
            self.resultEdit.clear()
            self.resultEdit.insertPlainText("格式错误，请重试")

    def GetSQLField(self):
        try:
            text = self.textEdit.toPlainText()
            s = "".join(str(text).split("\n"))
            aaa = re.split(r'CREATE(.+?)\(', s, 2)
            pattern = re.compile(r'`(.+?)((` varchar)|(` int)|(` date)|(` double)|(` datetime)|(` bit)|(` time))')
            a = re.findall(pattern, aaa[2])
            field = []
            for i in a:
                field.append(re.findall(r'^[A-Za-z0-9]+$', i[0])[0])
            self.resultEdit.clear()
            self.resultEdit.insertPlainText(",\n".join(str(i) for i in field))
        except:
            self.resultEdit.clear()
            self.resultEdit.insertPlainText("格式错误，请重试")

    def SqlFieldToBean(self):
        try:
            text = self.textEdit.toPlainText()
            lines = str(text).split("\n")
            aaa = []
            pattern = re.compile(r'`(.+?)((` varchar)|(` int)|(` double)|(` datetime)|(` bit))')
            typePattern = re.compile(r'varchar|int|double|datetime|bit')
            commentPattern = re.compile(r"COMMENT \'(.+?)'")
            titleText = ""
            for l in lines:
                if re.findall(pattern, l):
                    if re.findall(commentPattern, l):
                        tup = (
                            re.findall(pattern, l)[0][0], re.findall(typePattern, l)[0],
                            re.findall(commentPattern, l)[0])
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
            self.resultEdit.clear()
            self.resultEdit.insertPlainText(aText + ssefText)
        except:
            self.resultEdit.clear()
            self.resultEdit.insertPlainText("格式错误，请重试")

    def mapperToSql(self):
        try:
            text = self.textEdit.toPlainText()
            lines = str(text).split("\n")
            aaa = []
            typePattern = re.compile(r'(\w+\.){2}\w+')
            jdbcTypePattern = re.compile(r'INTEGER|VARCHAR|TIMESTAMP|BIT|CHAR')
            tableName = ""
            Map = {}

            for l in lines:
                if re.findall(typePattern, l):
                    tableNameBig = str(re.findall('type="(.*)"', l)[0]).split('.')[-1]
                    tableName = switch(tableNameBig)
                elif re.findall(jdbcTypePattern, l):
                    column = str(re.findall(r'"(.*?)"', l)[0])
                    jdbcType = str(re.findall(r'"(.*?)"', l)[1])
                    # 检查jdbcType是否正确
                    if getType(jdbcType) is not None:
                        Map[column] = jdbcType
                    else:
                        jdbcType = str(re.findall(r'"(.*?)"', l)[2])
                        Map[column] = jdbcType
            sqlStr = 'CREATE TABLE `%s` (\n' % (tableName)
            for k, v in Map.items():
                sqlPart = "`%s` %s NOT NULL,\n" % (k, getType(v))
                sqlStr = sqlStr + sqlPart
            sqlStr = sqlStr + "  PRIMARY KEY (`code`))  \n" \
                              "ENGINE=InnoDB DEFAULT CHARSET=utf8;"
            self.resultEdit.clear()
            self.resultEdit.insertPlainText(sqlStr)
        except:
            self.resultEdit.clear()
            self.resultEdit.insertPlainText("格式错误，请重试")

    def topysql(self):
        try:
            text = self.textEdit.toPlainText()
            s = ''
            for t in text.split('\n'):
                s = s + '"' + t + '"\\ \n'
            self.resultEdit.clear()
            self.resultEdit.insertPlainText(s)
        except:
            self.resultEdit.clear()
            self.resultEdit.insertPlainText("格式错误，请重试")

    def idFormat(self):
        try:
            text = self.textEdit.toPlainText()
            s = ''
            for t in text.split('\n'):
                s = s + "'" + t + "',\n"
            self.resultEdit.clear()
            self.resultEdit.insertPlainText(s)
        except:
            self.resultEdit.clear()
            self.resultEdit.insertPlainText("格式错误，请重试")


# 私有方法....................................................................
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


def switch(s):
    new_string = re.sub('[A-Z]+', lambda x: "_" + str(x.group(0)).lower(), s)
    if len(new_string) > 0:
        return new_string[1:]


def getType(v):
    oper = {
        'INTEGER': 'int',
        'VARCHAR': 'VARCHAR (32) ',
        'TIMESTAMP': 'datetime',
        'BIT': 'bit (1) ',
        'CHAR': 'char (32) '
    }
    return oper.get(v)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
