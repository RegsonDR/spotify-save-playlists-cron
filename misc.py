import os
from datetime import date, datetime

#getting env variable along with stripping
def get_env(name):
    if name in os.environ:
        return  os.environ.get(name).strip()
    return None


def get_weekday():
    return date.today().weekday()

def get_timestamp():
    datetime_obj = datetime.now()
    return datetime_obj