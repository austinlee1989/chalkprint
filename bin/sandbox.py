import MySQLdb
import pandas as pd

"""
First task is to import chalkprint data from MySQL DB into a pandas DF, from there build models classifying when
a user is actually climbing. Introduce magnitude of change of position and net acceleration, find when acceleration == 0
then we know a user is falling/dropping.
"""


def local_db_connect(query):
    mysql_cn = MySQLdb.connect(host='127.0.0.1',
                               port=3306, user='root', passwd='fnwl5r',
                               db='chalkprint')
    return pd.read_sql(query, con=mysql_cn)

"""Working script for in session analysis"""

data = local_db_connect("select * from chalkprint.bouldering_raw")
data['timeStamp'] = pd.to_datetime(data['timeStamp'], infer_datetime_format=True)
data.index = data['timeStamp']
del data['timeStamp']

grouped = data.groupby('session_id')

print(grouped.groups)

grouped['relAltitude'].plot()