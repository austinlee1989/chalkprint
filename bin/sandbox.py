import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt

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
grouped_is_climbing = data.groupby('isClimbing')

"""Create new columns for change in acceleration and change in rotation, group by session_id"""


def find_diff(data, var_names):
    return pd.Series(
        (sum([(data[i] - data[i].shift(-1)) ** 2 for i in var_names])) ** .5
        , index=data.index
    )

def find_direction(data, var_names):
    return pd.Series(
        [1 if (data[i] > data[i].shift(-1)) else 0 for i in var_names]
        ,index=data.index
    )

accel_to_loop = ["accelX", "accelY", "accelZ"]
rot_to_loop = ["rotX", "rotY", "rotZ"]
alt_to_loop = ["relAltitude"]

data['delta_accel'] = find_diff(data, accel_to_loop)
data['delta_rot'] = find_diff(data, rot_to_loop)
data['delta_alt'] = find_diff(data, alt_to_loop)

"""Set isClimbing Flag, start with 5 second rolling mean of altitude"""
""" Smoothing dataset, default window = 5 seconds"""
data['altRollingMean'] = pd.rolling_mean(data['relAltitude'], window=5)
data['delta_altRollingMean'] = pd.rolling_mean(data['delta_alt'], window=5)


""" Check for obvious breaks in rolling mean histogram"""
data.plot.hist()
data['altRollingMean'].hist(by=data['session_id'], bins=100)
data['delta_altRollingMean'].hist(by=data['session_id'], bins=100)

"""Find ground by taking rolling min across previous X minutes (method to find X minutes later)"""

min_lookback = 300
data['ground_level'] = pd.rolling_min(data['altRollingMean'], window=min_lookback)
data['alt_climbed'] = pd.rolling_max(data['altRollingMean'], window =5) - data['ground_level']

data.groupby('session_id').plot(data)



####
testing_dict = data_dict[data_dict.keys()[0]]
time_col = 'timeStamp'
ts = pd.to_datetime(testing_dict[time_col], infer_datetime_format=True)
# sec = pd.to_timedelta(ts, unit='s')
normed_sec = ts - min(ts)
self.data.index = normed_sec
del self.data[time_col]