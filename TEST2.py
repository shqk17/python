import datetime
import tkinter.messagebox
import os,uuid
import random
from tkinter import *
txt = open("./sql.txt","a",encoding="utf-8")
begin_date = datetime.datetime.strptime("2017-01-01", "%Y-%m-%d")
end_date = datetime.datetime.strptime("2017-12-31", "%Y-%m-%d")
while begin_date <= end_date:
    date_str = begin_date.strftime("%Y-%m-%d")
    begin_date += datetime.timedelta(days=1)
    s_uuid = str(uuid.uuid4())
    l_uuid = s_uuid.split('-')
    s_uuid = ''.join(l_uuid)
   ##s = "INSERT INTO `t_tss`.`tss_right_statistic_monthly_report_task_record` (`id`, `contractNumber`, `type`, `statisticDate`, `expendClassHour`, `returnPremiumAmount`, `returnPremiumClassHour`) VALUES ('{}', 'FFFFFFFFFFFFVVVV', '1','{}', '{}', '{}', '{}');\n".format(s_uuid,date_str,random.randint(1,100),random.randint(1,100),random.randint(1,100))
    s=""
    txt.write(s)
txt.close()

