import pandas as pd


RAW_FILE = "data/raw/commodities/commodity_prices.xlsx"

OUTPUT_FILE = (
    "data/processed/commodities/"
    "commodity_prices_processed.csv"
)


def preprocess_commodity_data():
    # Load monthly prices sheet
    df = pd.read_excel(
        RAW_FILE,
        sheet_name="Monthly Prices",
        header=4
    )

    # Rename date column
    df = df.rename(
        columns={
            "Unnamed: 0": "date"
        }
    )

    # Keep required commodities
    df = df[
        [
            "date",
            "Crude oil, average",
            "Natural gas, US",
            "Wheat, US SRW"
        ]
    ]

    # Rename columns
    df = df.rename(
        columns={
            "Crude oil, average": "oil",
            "Natural gas, US": "gas",
            "Wheat, US SRW": "wheat"
        }
    )

    # Convert dates
    df["date"] = pd.to_datetime(
        df["date"].str.replace("M", "-"),
        format="%Y-%m"
    )

    # Remove missing values
    df = df.dropna()

    # Sort chronologically
    df = df.sort_values("date")

    # Save processed data
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(df.head())
    print(df.tail())
    print(df.info())

    print(
        f"Processed data saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    preprocess_commodity_data()