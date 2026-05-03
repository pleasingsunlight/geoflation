import joblib

MODEL_PATH = "backend/ml_models/model.joblib"

_model = None


def get_model():
    global _model

    if _model is None:
        _model = joblib.load(MODEL_PATH)

    return _model