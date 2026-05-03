import pandas as pd


def build_features(df: pd.DataFrame):
    df = df.copy()

    # Encode categorical variables
    df = pd.get_dummies(df, columns=["event_type", "sector"])

    # Features
    feature_cols = [col for col in df.columns if col not in [
        "oil_price_change",
        "gas_price_change",
        "delay_weeks",
        "country"
    ]]

    X = df[feature_cols]

    # Targets
    y = df[["oil_price_change", "gas_price_change", "delay_weeks"]]

    return X, y

def build_features_from_event(event):

    data = {
        "event_type": [event.event_type.value],
        "sector": [event.sector.value],
        "severity": [event.severity],
        "country": [event.country],
    }

    df = pd.DataFrame(data)

    # Apply same encoding as training
    df = pd.get_dummies(df, columns=["event_type", "sector"])

    return df