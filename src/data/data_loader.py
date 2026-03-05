from pathlib import Path
import numpy as np
import pandas as pd
import datetime
import os
from dotenv import load_dotenv
from src.data.time_series import get_ar_terms, get_lag_dict, crop_by_lags

# Get the directory of the current module
module_dir = Path(__file__).resolve().parent

# Construct the path to the .env file
dotenv_path = module_dir / '.env'

# Load the .env file
if dotenv_path.is_file():
    load_dotenv(dotenv_path=dotenv_path)
else:
    # Handle the case where the .env file is not found
    print(f"Warning: .env file not found at {dotenv_path}")

PROCESSED_INDEX_DATA = os.getenv('PROCESSED')
TARGET = 'Delta Close'

class DataLoader:
    def __init__(self, processed_path=PROCESSED_INDEX_DATA,
            index='NYA', earliest_date=datetime.datetime(year=2003,month=1,day=9),
            test_size=0.2, rolling_window=7, pacf_alpha=0.1, include_adj_close=False):
        self.processed_index_path = Path.joinpath(module_dir,processed_path)
        self.index = index
        self.earliest_date = earliest_date
        self.test_size = test_size
        self.rolling_window = rolling_window
        self.pacf_alpha = pacf_alpha
        self.include_adj_close = include_adj_close
        self.processed_index_df = None
        self.prepared_df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def load_processed_data(self):
        """load processed index data from csv file. parse dates in column 1 as datetime objects
        assign result to self.processed_index_df
        """
        self.processed_index_df = pd.read_csv(self.processed_index_path, parse_dates=[1])

    @staticmethod
    def filter_by_index(processed_index_df, index):
        """filter processed index data to only include rows for the stock index specified in self.index
        assign result to self.processed_index_df"""
        return processed_index_df[processed_index_df['Index'] == index]
    
    @staticmethod
    def filter_by_date(processed_index_df, earliest_date):
        """filter processed index data to only include rows from the date specified in self.earliest_date onwards
        assign result to self.processed_index_df"""
        return processed_index_df[processed_index_df['Date'] >= earliest_date]
    
    def filter_processed_data(self):
        self.load_processed_data()
        filtered_df = DataLoader.filter_by_index(self.processed_index_df, self.index)
        filtered_df = DataLoader.filter_by_date(filtered_df, self.earliest_date)
    
        filtered_df = filtered_df.set_index('Date')
        filtered_df.drop(columns=['Index', 'CloseUSD'], inplace=True)
        return filtered_df

    @staticmethod
    def shift_closing(processed_index_df):
        #opening price of day n is closing price of day n-1
        processed_index_df.rename(columns={'Open':'Last Close', 'Adj Close': 'Last Adj Close'},inplace=True)
        #align target (next day's close) with predictors
        processed_index_df['Close'] = processed_index_df['Close'].shift(-1)
        #align last adjust closing price with last closing price
        processed_index_df['Last Adj Close'] = processed_index_df['Last Adj Close'].shift(1)
        processed_index_df.dropna(inplace=True)
        return processed_index_df
    
    @staticmethod
    def engineer_features(filtered_df):
        """perform feature engineering and return result"""
        #high and low prices are highly correlated with the last closing price
        #instead use high and low values as proportions of last closing price
        filtered_df['LowProportion'] = filtered_df['Low']/filtered_df['Last Close']
        filtered_df['HighProportion'] = filtered_df['High']/filtered_df['Last Close']
        filtered_df.drop(columns=['High', 'Low'], inplace=True)
        return filtered_df
    
    def prepare_df(self):
        """prepare Dataframe filtered to single index and from earliest date. Manipulate columns as 
        stipulated by engineer_features. Create column for daily delta closing price."""
        self.prepared_df = self.filter_processed_data()
        self.prepared_df = DataLoader.shift_closing(self.prepared_df)
        #engineer features and assign to self.X
        self.prepared_df = self.engineer_features(self.prepared_df)
        #create column for delta close, which will serve as target
        self.prepared_df['Delta Close'] = self.prepared_df['Close'] - self.prepared_df['Last Close']
        #compute lag dataframe using PACF from only training data
        train_series = DataLoader.time_split_1D(self.prepared_df['Delta Close'],test_size=self.test_size)[0]
        ar_terms = get_ar_terms(train_series, rolling_window=self.rolling_window, alpha=self.pacf_alpha)
        lag_dict = get_lag_dict(self.prepared_df['Delta Close'], ar_terms)
        self.prepared_df = crop_by_lags(self.prepared_df,ar_terms)
        self.prepared_df = self.prepared_df.assign(**lag_dict)
        return self.prepared_df
    
    def prepare_X(self):
        self.prepare_df()
        self.X = self.prepared_df.drop(columns=['Last Close', 'Close', TARGET])
        if not self.include_adj_close:
            self.X.drop(columns=['Last Adj Close'], inplace=True)
        return self.X
    
    def prepare_y(self):
        self.prepare_df()
        #separate target series from features
        self.y = self.prepared_df[TARGET]
        #quantize for classification problem according to 0 if <=0 and 1 otherwise
        self.y = DataLoader.quantize_delta_close(self.y)
        return self.y
    
    def prepare_X_y(self):
        return self.prepare_X(), self.prepare_y()
    
    @staticmethod
    def time_split_2D(data, test_size=0.2):
        cut_index = int((1-test_size)*data.shape[0])
        train_data = data.iloc[:cut_index,:]
        test_data = data.iloc[cut_index:,:]
        return train_data, test_data
    
    @staticmethod
    def time_split_1D(data, test_size=0.2):
        cut_index = int((1-test_size)*len(data))
        train_data = data[:cut_index]
        test_data = data[cut_index:]
        return train_data, test_data

    
    def train_test_split(self):
        """perform temporal train test split according to proportion in self.test_size"""
        #load X, y if not already loaded
        if self.X is None:
            self.prepare_X()
        if self.y is None:
            self.prepare_y()

        self.X_train, self.X_test = DataLoader.time_split_2D(self.X, self.test_size)
        self.y_train, self.y_test = DataLoader.time_split_1D(self.y, self.test_size)
    
    @staticmethod
    def quantize_delta_close(delta_close):
        """return array of 0 if <= 0 and 1 if > 0"""
        return pd.Series(data=[0 if y <= 0 else 1 for y in delta_close], index=delta_close.index)

        

    

    