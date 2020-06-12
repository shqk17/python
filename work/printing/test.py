import datetime


class Printer(object):

    @staticmethod
    def getTime():
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return nowTime


if __name__ == '__main__':
    logger = open(
        "./" + datetime.datetime.now().strftime('%Y-%m') + "main.log",
        "a", encoding="utf-8")
    logger.write(Printer.getTime() + "--main --测试--\n")
    logger.close()
