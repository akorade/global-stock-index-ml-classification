from pathlib import Path
import pickle
import numpy as np
from data.data_loader import DataLoader
from tune_rf import tune_model

#a movement of h index points corresponds to a h*CONTRACT_MULTIPLIER movement in dollars
CONTRACT_MULTIPLIER = 100
#leverage of the trading position is 1/MARGIN:1
MARGIN = 0.05

SCRIPT_DIR = Path(__file__).resolve().parent
MODEL_NAME = 'rf_model.pkl'

def execute_trades(y_pred, delta_close):
    num_contracts = 0
    funds = 0
    for i, y in enumerate(y_pred):
        if y == 0:
            num_contracts -= 1
        else:
            num_contracts += 1
        funds += num_contracts*CONTRACT_MULTIPLIER*delta_close[i]/MARGIN
    return funds

def rf_trade():
    root_dir = Path(SCRIPT_DIR).resolve().parent
    model_path = Path.joinpath(root_dir, 'models', MODEL_NAME)

    if not model_path.exists():
        tune_model()

    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    
    dl = DataLoader()
    _, X_test, _, y_test = dl.train_test_split()
    _, price_df = DataLoader.time_split_2D(dl.prepared_df)
    delta_close = price_df['Delta Close'].values
    
    y_pred = model.predict(X_test)
    funds = execute_trades(y_pred, delta_close)
    
    print(f"Random Forest funds = ${round(funds,2):,}")

def baseline_trade():
    """predict 0 for the first index. For each index afterwards, predict the previous value in the time series"""
    dl = DataLoader()
    _, price_df = DataLoader.time_split_2D(dl.prepare_df())
    delta_close = price_df['Delta Close'].values

    y_pred = np.zeros(len(delta_close))
    for i, val in enumerate(delta_close[1:]):
        y_pred[i] = delta_close[i-1]
    
    funds = execute_trades(y_pred, delta_close)

    print(f"Baseline funds = ${round(funds,2):,}")
        




if __name__ == '__main__':
    baseline_trade()
    rf_trade()