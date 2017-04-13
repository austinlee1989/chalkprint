import MySQLdb
import pandas as pd
import math

"""
First task is to import chalkprint data from MySQL DB into a pandas DF, from there build models classifying when
a user is actually climbing. Introduce magnitude of change of position and net acceleration, find when acceleration == 0
then we know a user is falling/dropping. Set the height climbed = max(height before accel = 0) - min(height at climb start)
time logic is set using the same logic
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

"""Create new columns for change in acceleration and change in rotation, group by session_id"""

def find_diff(data_column):
        return data_column - data_column.shift(-1)

var_to_loop = ["accelX", "accelY", "accelZ"]

data['delta_accel'] = pd.Series(
    (sum([find_diff(data[i])**2 for i in var_to_loop]))**.5/len(var_to_loop)
    , index=data.index
)

data['delta_accelX'] = pd.Series(find_diff(data['accelX'])**2, index=data.index)
data['delta_accelY'] = pd.Series(find_diff(data['accelY'])**2, index=data.index)
data['delta_accelZ'] = pd.Series(find_diff(data['accelZ'])**2, index=data.index)



