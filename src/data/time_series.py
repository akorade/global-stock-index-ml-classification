
from statsmodels.tsa.stattools import pacf
import numpy as np
import pandas as pd

def get_ar_terms(series, rolling_window=1, alpha=0.1):
    """computes significant autoregressive terms from a Partial Autocorrelation Function (PACF)
    rolling window: size of the rolling mean window to be used on series for smoothing
    alpha: significance threshold for PAC
    returns autoregressive terms to be used 
    """
    series_pacf = pacf(series.rolling(window=rolling_window).mean().dropna(), method='ywm')
    ar_terms = [i for i,val in enumerate(np.abs(series_pacf) > alpha) if val]
    ar_terms = ar_terms[1:]
    return ar_terms

def get_lag_dict(series, ar_terms):
    """prepares a dataframe of lags from a series"""
    name = 'y'
    if isinstance(series, pd.Series) and series.name is not None:
        name = series.name

    p = max(ar_terms)
    lag_dict = {}
    for j in ar_terms:
        col_name = f'{name}_(t-{j})'
        lag_dict[col_name] = []
    for i in range(p,len(series)):
        for j in ar_terms:
            col_name = f'{name}_(t-{j})'
            lag_val = series.iloc[i-j]
            lag_dict[col_name].append(lag_val)
    return lag_dict

def crop_by_lags(df, ar_terms):
    p = max(ar_terms)
    return df.iloc[p:,:]
