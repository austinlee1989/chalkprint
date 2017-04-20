from scipy.signal import savgol_filter
import pandas as pd

def find_diff(self, var_names):
    """
    The find diff function finds the total scalar difference between the any two vectors, a rolling mean can then
     be calculated to find the mean rate of change per second, allow us
     to detect periods of increased activity and movement.
     """
    return pd.Series(
        (sum([(self.data[i] - self.data[i].shift(-1)) ** 2 for i in self.feature_names])) ** .5
        , index=self.data.index)

def smooth_series(self, column, interval, method):
    if method == 'savgol':
        savgol_filter(self.series, window_length=interval, polyorder=2)
    elif method == 'rolling_mean':
        pd.rolling_mean(self.series, window=interval)