import joblib
from sklearn.ensemble import RandomForestRegressor

from backend.data_pipeline.ingestion import load_data
from backend.data_pipeline.preprocessing import preprocess
from backend.data_pipeline.feature_engineering import build_features


MODEL_PATH = "backend/ml_models/model.joblib"


def train_model():
    df = load_data("data/raw/events.csv")
    df = preprocess(df)
    X, y = build_features(df)

    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    print("Model trained and saved at:", MODEL_PATH)


def predict(X):
    model = joblib.load(MODEL_PATH)
    return model.predict(X)


if __name__ == "__main__":
    train_model()