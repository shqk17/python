import datetime as datetime

def date_add_seconds(str_time):
    time_old = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    time_offset = time_old+datetime.timedelta(seconds=1)
    return time_offset.strftime("%Y-%m-%d %H:%M:%S")

