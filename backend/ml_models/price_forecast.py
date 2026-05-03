from backend.data_pipeline.ingestion import load_data
from backend.data_pipeline.preprocessing import preprocess
from backend.data_pipeline.feature_engineering import build_features


def train_model():
    df = load_data("data/raw/events.csv")
    df = preprocess(df)
    X, y = build_features(df)

    print("Training data shape:", X.shape)
    print("Targets shape:", y.shape)

    # Placeholder (real model comes next step)
    return {
        "status": "training_stub_complete"
    }


if __name__ == "__main__":
    train_model()