import joblib

MODEL_PATH = "backend/ml_models/model.joblib"

_model_data = None


def get_model():
    global _model_data

    if _model_data is None:
        _model_data = joblib.load(MODEL_PATH)

    return _model_data["model"], _model_data["columns"]