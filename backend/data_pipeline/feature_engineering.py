import pandas as pd


def build_features(df: pd.DataFrame):
    df = df.copy()

    # New engineered features
    df["is_energy"] = (df["sector"] == "energy").astype(int)
    df["is_conflict"] = df["event_type"].isin(["war"]).astype(int)
    df["high_severity"] = (df["severity"] > 0.7).astype(int)

    # One-hot encoding
    df = pd.get_dummies(df, columns=["event_type", "sector"])

    feature_cols = [col for col in df.columns if col not in [
        "oil_price_change",
        "gas_price_change",
        "delay_weeks",
        "country"
    ]]

    X = df[feature_cols]
    y = df[["oil_price_change", "gas_price_change", "delay_weeks"]]

    return X, y

def build_features_from_event(event):
    import pandas as pd

    df = pd.DataFrame([{
        "event_type": event.event_type.value,
        "sector": event.sector.value,
        "severity": event.severity,
        "country": event.country,
    }])

    # SAME engineered features
    df["is_energy"] = (df["sector"] == "energy").astype(int)
    df["is_conflict"] = (df["event_type"] == "war").astype(int)
    df["high_severity"] = (df["severity"] > 0.7).astype(int)

    df = pd.get_dummies(df, columns=["event_type", "sector"])

    return df