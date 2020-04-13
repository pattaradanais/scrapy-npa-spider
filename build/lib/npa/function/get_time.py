from datetime import datetime
import pytz

def now_string_with_timezone():
    now = datetime.now()
    bkk_tz = pytz.timezone('Asia/Bangkok')
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    bkk_dt = now.astimezone(bkk_tz)
    dt_string = bkk_dt.strftime(fmt)
    return dt_string

def now_string():
    now = datetime.now()
    bkk_tz = pytz.timezone('Asia/Bangkok')
    fmt = '%Y-%m-%d %H:%M:%S'
    bkk_dt = now.astimezone(bkk_tz)
    dt_string = bkk_dt.strftime(fmt)
    return dt_string