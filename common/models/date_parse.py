from datetime import datetime, time, date, timedelta

def parse_timedelta(time_str: str) -> timedelta:
    try:
        days, hours, minutes = map(int, time_str.split('-'))
        return timedelta(days=days, hours=hours, minutes=minutes)
    except ValueError:
        raise ValueError("Niepoprawny format. Oczekiwany format: 'dd-hh-mm'")

def parse_datetime(str_datetime: str):
    splitted = str_datetime.split(' ')

    if len(splitted) > 1:
        v_date = parse_date(str_datetime.split(' ')[0])
        v_time = parse_time(str_datetime.split(' ')[1])

        return datetime(v_date.year, v_date.month, v_date.day, v_time.hour, v_time.minute, v_time.second)
    else:
        v_date = parse_date(str_datetime.split(' ')[0])

        return datetime(v_date.year, v_date.month, v_date.day, 0,0,0)

# dd-mm-yyyy
def parse_date(str_date:str):
    str_date = str_date.lower()
    if str_date == "today":
        return date.today()

    splitted = str_date.split('-')

    d = int(splitted[0])
    m = int(splitted[1])
    y = int(splitted[2])

    return date(y,m,d)

# hh-mm-ss
def parse_time(str_time: str):
    str_time = str_time.lower()
    if str_time == "now":
        now = datetime.now()
        return time(now.hour,now.minute, now.second)

    splitted = str_time.split('-')

    if len(splitted) < 3:
        splitted[2] = "00"

    h = int(splitted[0])
    m = int(splitted[1])
    s = int(splitted[2])

    return time(h, m, s)
