import MySQLdb
import pandas as pd

"""
First task is to import chalkprint data from MySQL DB into a pandas DF, from there build models classifying when
a user is actually climbing. Introduce magnitude of change of position and net acceleration, find when acceleration == 0
then we know a user is falling/dropping. Periods of high variance in acceleration/rotation may also indicate periods
when user is actually climbing as well.
We can find the ground altitude by taking the rolling minimum value of the rolling mean relative altitude across X
periods. After this, the rolling maximum is found over a much shorter period, after

Create a clean DF for each session using bouldering method, then use unsupervised learning (clustering)
, find 'clusters' of behavior from smoothed series
"""


def local_db_connect(query):
    mysql_cn = MySQLdb.connect(host='127.0.0.1',
                               port=3306, user='root', passwd='fnwl5r',
                               db='chalkprint')
    return pd.read_sql(query, con=mysql_cn)


class Bouldering:

    def __init__(self, dataframe):
        self.data = dataframe

    def data_frame(self):
        return self.data

    def set_time_index(self, time_col):
        """
        Coerce the time column into datetime format, index on new column so that time series analysis is possible
        and then delete the column to free up memory (values persist in index)
        """
        self.data.index = pd.to_datetime(self.data[time_col], infer_datetime_format=True)
        del self.data[time_col]

    def find_diff(self, var_names):
        """
        The find diff function finds the scalar difference between the any two vectors, note that direction isn't
         propogated here, a rolling mean can then be calculated to find the mean rate of change per second, allow us
         to detect periods of increased activity and movement.
         """
        return pd.Series(
            (sum([(self.data[i] - self.data[i].shift(-1)) ** 2 for i in var_names])) ** .5
            , index=self.data.index)

    def set_group_id(self, id_name):
        return self.data.groupby(id_name)


"""Global Variables/Lists"""

accel_to_loop = ["accelX", "accelY", "accelZ"]
rot_to_loop = ["rotX", "rotY", "rotZ"]
alt_to_loop = ["relAltitude"]
query_raw = "select * from chalkprint.bouldering_raw"

if __name__ == "__main__":
    input_data = local_db_connect(query_raw)
    data_dict = {}
    group_id = 'session_id'
    for name, group in input_data.groupby(group_id):
        data_dict[name] = group.drop(group_id, axis=1)


    data = Bouldering(input_data)
    print(input_data)

