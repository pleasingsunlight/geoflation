import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from backend.data_pipeline.ingestion import load_data
from backend.data_pipeline.preprocessing import preprocess
from backend.data_pipeline.feature_engineering import build_features


MODEL_PATH = "backend/ml_models/model.joblib"


def train_model():
    df = load_data("data/raw/events.csv")
    df = preprocess(df)
    X, y = build_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    error = mean_absolute_error(y_test, preds)

    print("MAE:", round(error, 2))

    joblib.dump({
        "model": pipeline,
        "columns": X.columns.tolist()
    }, MODEL_PATH)

    print("Model trained and saved.")
    

def predict(X):
    model = joblib.load(MODEL_PATH)
    return model.predict(X)


if __name__ == "__main__":
    train_model()