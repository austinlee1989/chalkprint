import MySQLdb
import pandas as pd

"""
First task is to import chalkprint data from MySQL DB into a pandas DF, from there build models classifying when
a user is actually climbing. Introduce magnitude of change of position and net acceleration, find when acceleration == 0
then we know a user is falling/dropping. Periods of high variance in acceleration/rotation may also indicate periods
when user is actually climbing as well.
"""


def local_db_connect(query):
    mysql_cn = MySQLdb.connect(host='127.0.0.1',
                               port=3306, user='root', passwd='fnwl5r',
                               db='chalkprint')
    return pd.read_sql(query, con=mysql_cn)


def convert_for_timeseries(time_column):
    return pd.to_datetime(time_column, infer_datetime_format=True)
"""
class Bouldering:

    def __init__(self):

"""


if __name__ == "__main__":
    data = local_db_connect("select * from chalkprint.bouldering_raw")
    print(data)