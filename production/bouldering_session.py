import MySQLdb
import pandas as pd
from scipy.signal import savgol_filter

"""
First task is to import chalkprint data from MySQL DB into a pandas DF, from there build models classifying when
a user is actually climbing. Introduce magnitude of change of position and net acceleration, find when acceleration == 0
then we know a user is falling/dropping. Periods of high variance in acceleration/rotation may also indicate periods
when user is actually climbing as well.
We can find the ground altitude by taking the rolling minimum value of the rolling mean relative altitude across X
periods. After this, the rolling maximum is found over a much shorter period, after

Create a clean DF for each session using bouldering method, then use unsupervised learning (clustering)
, find 'clusters' of behavior from smoothed series

Process:
1. Smooth Data
2. Define Magnitude of change in Accel and Rotation between periods
4. Use simple heuristics to flag 'is_climbing' start
    a. establish start = acceleration + delta_altitude is positive for more than 5 seconds
    b. establish end = acceleration goes to zero
5. Establish 'floor' trendline


"""


def local_db_connect(query):
    mysql_cn = MySQLdb.connect(host='127.0.0.1',
                               port=3306, user='root', passwd='fnwl5r',
                               db='chalkprint')
    return pd.read_sql(query, con=mysql_cn)


class BoulderingSession:

    def __init__(self, dataframe):
        self.data = dataframe

    def data_frame(self):
        return self.data

    def set_time_index(self, time_col):
        """
        Coerce the time column into datetime format, index on new column so that time series analysis is possible
        and then delete the column to free up memory (values persist in index), create column of seconds since start of
        session, then index on column
        """
        ts = pd.to_datetime(self.data[time_col], infer_datetime_format=True)
        self.data.index = (ts - min(ts))/10**9
        #pd.timestamp defaults to nanoseconds, dividing by 10^9 converts to sec
        del self.data[time_col]

    def find_diff(self, var_names):
        """
        The find diff function finds the total scalar difference between the any two vectors, a rolling mean can then
         be calculated to find the mean rate of change per second, allow us
         to detect periods of increased activity and movement.
         """
        return pd.Series(
            (sum([(self.data[i] - self.data[i].shift(-1)) ** 2 for i in var_names])) ** .5
            , index=self.data.index)

    def smooth_series(self, column, interval, method):
        col_name = column + "_smooth_" + str(interval)
        if method == 'savgol':
            self.data[col_name] = savgol_filter(self.data[column], window_length=interval, polyorder=2)
        elif method == 'rolling_mean':
            self.data[col_name] = pd.rolling_mean(self.data[column], window=interval)


"""Global Variables/Lists"""

accel_to_loop = ["accelX", "accelY", "accelZ"]
rot_to_loop = ["rotX", "rotY", "rotZ"]
alt_to_loop = ["relAltitude"]
query_raw = "select * from chalkprint.bouldering_raw"

if __name__ == "__main__":
    input_data = local_db_connect(query_raw)
    data_dict = {}
    group_id = 'session_id'
    smooth_interval = 5
    for name, group in input_data.groupby(group_id):
        data_dict[name] = group.drop(group_id, axis=1)

    for session in data_dict:
        session_bouldering = BoulderingSession(data_dict[session])
        session_bouldering.set_time_index('timeStamp')
        session_bouldering.smooth_series(column='relAltitude', interval=5, method='rolling_mean')
        out_data = session_bouldering.data_frame()
        print(out_data[:10])
        out_data[['relAltitude', 'relAltitude_smooth_5']][1500:1800].plot()

