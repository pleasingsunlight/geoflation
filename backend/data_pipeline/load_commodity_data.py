import pandas as pd


def load_commodity_data():
    file_path = "data/raw/commodities/commodity_prices.xlsx"

    df = pd.read_excel(file_path, sheet_name="Monthly Prices", header=4)

    return df


if __name__ == "__main__":
    df = load_commodity_data()

    print(df.head())
    print(df.columns)