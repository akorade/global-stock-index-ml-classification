from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, cross_val_score, GridSearchCV
import pickle
import os
from pathlib import Path

from data.data_loader import DataLoader

SCRIPT_DIR = Path(__file__).resolve().parent

MODEL_NAME = 'rf_model.pkl'

def tune_model():
    root_dir = Path(SCRIPT_DIR).resolve().parent
    model_dir = Path.joinpath(root_dir, 'models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = Path.joinpath(model_dir, MODEL_NAME)

    dl = DataLoader(test_size = 0.2)
    X, y = dl.prepare_X_y()

    X_train, X_test, y_train, y_test = dl.train_test_split()

    param_grid = {
        'n_estimators': [100, 200, 300, 400, 500],
        'max_depth': [None, 5, 10, 15, 20],
        'min_samples_split': [2, 5, 10]
    }

    tscv = TimeSeriesSplit(n_splits=5) 

    rf = RandomForestClassifier(random_state=42)

    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=tscv,
        scoring='neg_log_loss',
        refit=True, # Refit an estimator using the best found parameters on the whole dataset
        n_jobs=-1
    )

    print('Performing hyperparameter grid search')
    grid_search.fit(X_train, y_train)

    print(f'Saving best model to {str(model_path)}')
    best_rf = grid_search.best_estimator_

    try:
        with open(model_path, 'wb') as file:
            pickle.dump(best_rf, file)
        print(f"Model successfully saved to {str(model_path)}")
    except Exception as e:
        print(f"An error occurred: {e}")


    print(f"Best parameters found: {grid_search.best_params_}")
    print(f"Best cross-validation score: {grid_search.best_score_}")


    y_pred = best_rf.predict(X_test)
    y_prob = best_rf.predict_proba(X_test)[:,1]

    print("Random Forest Accuracy:", best_rf.score(X_test, y_test))
    print(classification_report(y_test, y_pred))
    print("ROC-AUC:", roc_auc_score(y_test, y_prob))

if __name__ == "__main__":
    tune_model()

