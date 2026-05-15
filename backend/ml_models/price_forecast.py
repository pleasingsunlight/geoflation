import pandas as pd

from prophet import Prophet


DATA_FILE = (
    "data/processed/commodities/"
    "commodity_prices_processed.csv"
)


def load_data():
    return pd.read_csv(
        DATA_FILE,
        parse_dates=["date"]
    )


def forecast_commodity(column_name, periods=12):
    df = load_data()

    commodity_df = df[
        ["date", column_name]
    ].rename(
        columns={
            "date": "ds",
            column_name: "y"
        }
    )

    commodity_df["y"] = pd.to_numeric(
        commodity_df["y"],
        errors="coerce"
    )

    commodity_df = commodity_df.dropna(subset=["y"])

    model = Prophet()

    model.fit(commodity_df)

    future = model.make_future_dataframe(
        periods=periods,
        freq="ME"
    )

    forecast = model.predict(future)

    result = forecast[
        ["ds", "yhat"]
    ].tail(periods)

    return [
        {
            "date": row["ds"].strftime("%Y-%m-%d"),
            "price": round(row["yhat"], 2)
        }
        for _, row in result.iterrows()
    ]