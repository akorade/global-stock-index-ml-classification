from pathlib import Path
import numpy as np
import pandas as pd
import datetime
import os
from dotenv import load_dotenv

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

class DataLoader:
    def __init__(self, processed_path=PROCESSED_INDEX_DATA,
            index='NYA', earliest_date=datetime.datetime(year=2004,month=1,day=1),
            test_size=0.2):
        self.processed_index_path = Path.joinpath(module_dir,processed_path)
        self.index = index
        self.earliest_date = earliest_date
        self.test_size = test_size
        self.processed_index_df = None
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
    
    def load_X_y(self):
        """perform feature engineering and split data into features X and target y
        assign results to self.X and self.y"""
        #load processed index data if not already loaded
        if not self.processed_index_df:
            self.load_processed_data()
        #filter down to only specified stock index
        index_mask = self.processed_index_df['Index'] == self.index
        #if an earliest date was specified, take only from that date onwards
        if self.earliest_date:
            date_mask = self.processed_index_df['Date'] >= self.earliest_date
        one_index_df = (self.processed_index_df[index_mask & date_mask]
            .set_index('Date').drop(columns=['Index', 'CloseUSD']))
        
        #opening price of day n is closing price of day n-1
        one_index_df.rename(columns={'Open':'Last Close', 'Adj Close': 'Last Adj Close'},inplace=True)
        #align target (next day's close) with predictors
        one_index_df['Close'] = one_index_df['Close'].shift(-1)
        #align last adjust closing price with last closing price
        one_index_df['Last Adj Close'] = one_index_df['Last Adj Close'].shift(1)
        one_index_df.dropna(inplace=True)

        #separate target series from features
        target = 'Close'
        self.y = one_index_df[target]

        #separate features from target
        self.X = one_index_df.drop(columns=[target])
        #high and low prices are highly correlated with the last closing price
        #instead use high and low values as proportions of last closing price
        self.X['LowProportion'] = self.X['Low']/self.X['Last Close']
        self.X['HighProportion'] = self.X['High']/self.X['Last Close']
        self.X.drop(columns=['High', 'Low'], inplace=True)
    
    def train_test_split(self):
        """perform temporal train test split according to proportion in self.test_size"""

        #load X, y if not already loaded
        if not self.X or not self.y:
            self.load_X_y()
        
        train_index = int((1-self.test_size)*self.X.shape[0])

        self.X_train = self.X.iloc[:train_index,:]
        self.X_test = self.X.iloc[train_index:,:]

        self.y_train = self.y[:train_index]
        self.y_test = self.y[train_index:]

        

    

    