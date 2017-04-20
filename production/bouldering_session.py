import pandas as pd
import processtools as pt
import local_connection


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

class BoulderingSession(object):

    def __init__(self, dataframe):
        self.data = dataframe
        self.acceleration = ["accelX", "accelY", "accelZ"]
        self.rotation = ["rotX", "rotY", "rotZ"]
        self.altitude = "relAltitude"

    def set_time_index(self, time_col):
        """
        Coerce the time column into datetime format, index on new column so that time series analysis is possible
        and then delete the column to free up memory (values persist in index), create column of seconds since start of
        session, then index on column
        """
        ts = pd.to_datetime(self.data[time_col], infer_datetime_format=True)
        self.data.index = ts - min(ts)
        #pd.timestamp defaults to nanoseconds, dividing by 10^9 converts to sec
        del self.data[time_col]

    def find_ground(self, min_interval=301, smooth_interval=29):
        """input smoothed relAltitude"""
        s_ = pt.smooth_series(column=self.altitude, interval=smooth_interval)
        return pd.rolling_min(s_, window=min_interval)

    def find_problem_start(self):



"""Global Variables/Lists"""

accel_to_loop = ["accelX", "accelY", "accelZ"]
rot_to_loop = ["rotX", "rotY", "rotZ"]
alt_to_loop = ["relAltitude"]
query_raw = "select * from chalkprint.bouldering_raw"

if __name__ == "__main__":
    input_data = local_connection.local_db_connect(query_raw)
    data_dict = {}
    group_id = 'session_id'
    smooth_interval = 5
    for name, group in input_data.groupby(group_id):
        data_dict[name] = group.drop(group_id, axis=1)

    for session in data_dict:
        sess = BoulderingSession(data_dict[session])
        sess.set_time_index('timeStamp')
        sess.smooth_series(column='relAltitude', interval=29, method='savgol')
        sess.find_ground()
        print(dir(sess))
        out_data = sess.data_frame
        out_data['ground'] = sess.find_ground()
        out_data[['delta_accel']] = sess.find_diff(accel_to_loop)
        #print(sess.find_diff(accel_to_loop))
        out_data[['delta_alt']] = sess.find_diff(['relAltitude_smoothed'])
        #print(out_data[:10])
        out_data[['relAltitude', 'relAltitude_smoothed','ground']].plot()
        out_data[['relAltitude_smoothed', 'delta_accel', 'delta_alt']].plot()

