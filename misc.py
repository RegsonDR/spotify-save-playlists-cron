import os
from datetime import date

#getting env variable along with stripping
def get_env(name):
    if name in os.environ:
        return  os.environ.get(name).strip()
    return None


def get_weekday():
    return date.today().weekday()