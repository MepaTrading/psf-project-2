import pandas as pd

def save_to_csv(dataframe, path):
    dataframe.to_csv(path)

def csv_to_dataframe(path):
    df = pd.read_csv('data/aapl.csv')