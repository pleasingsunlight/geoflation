import pandas as pd


def preprocess(df: pd.DataFrame):
    df = df.copy()

    # Normalize text
    df["event_type"] = df["event_type"].str.lower()
    df["sector"] = df["sector"].str.lower()

    return df