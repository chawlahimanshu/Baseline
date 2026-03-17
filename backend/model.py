import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import time

from data_pipeline import get_player_stats, get_player_id

def build_features(df):
    df = df.sort_values('GAME_DATE').reset_index(drop=True)
    df['HOME'] = df['MATCHUP'].apply(lambda x: 1 if 'vs.' in x else 0)
    df['OPPONENT'] = df['MATCHUP'].apply(lambda x: x.split('vs.')[1].strip() if 'vs.' in x else x.split('@')[1].strip())

    df['PTS_last_5'] = df['PTS'].rolling(5).mean().shift(1)
    df['PTS_last_10'] = df['PTS'].rolling(10).mean().shift(1)
    df['PTS_vs_opponent'] = df.groupby('OPPONENT')['PTS'].transform(lambda x: x.shift(1).expanding().mean())

    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    df['DAYS_REST'] = df['GAME_DATE'].diff().dt.days
    df['MIN_last_5'] = df['MIN'].rolling(5).mean().shift(1)
    df['YEAR'] = df['GAME_DATE'].dt.year
    df = df.dropna()

    return df
def train_model(df):
    features = ['HOME', 'PTS_last_5', 'PTS_last_10', 'PTS_vs_opponent', 'DAYS_REST', 'MIN_last_5', 'YEAR']
    X = df[features]
    y = df['PTS']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=3)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"MAE: {mae}")
    return model

def predict(model, df, opponent, home):
    # Get the most recent row as current form
    latest = df.iloc[-1].copy()
    
    # Set tonight's conditions
    latest['OPPONENT'] = opponent
    latest['HOME'] = home
    
    # Build the feature row
    features = ['HOME', 'PTS_last_5', 'PTS_last_10', 'PTS_vs_opponent', 'DAYS_REST', 'MIN_last_5', 'YEAR']
    X = latest[features].values.reshape(1, -1)
    
    # Make prediction
    prediction = model.predict(X)[0]
    print(f"\nPredicted points: {round(prediction, 1)}")
    return prediction

if __name__ == "__main__":
    player = input("Enter player name: ")
    opponent = input("Enter opponent (e.g. BOS): ")
    home = int(input("Home or away? (1 for home, 0 for away): "))
    
    df = get_player_stats(player)
    df = build_features(df)
    model = train_model(df)
    predict(model, df, opponent, home)

