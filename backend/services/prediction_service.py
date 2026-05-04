from backend.models.schemas import EventInput, PredictionResponse
from backend.ml_models.model_loader import get_model
from backend.data_pipeline.feature_engineering import build_features_from_event
from backend.ml_models.gnn_model import propagate_shock


def predict_event_impact(event: EventInput) -> PredictionResponse:
    try:
        model, columns = get_model()

        X = build_features_from_event(event)

        # Align columns with training
        for col in columns:
            if col not in X.columns:
                X[col] = 0

        X = X[columns]

        preds = model.predict(X)[0]

        oil, gas, delay = preds

        shock_map = propagate_shock(event.country, event.severity)
        affected_regions = list(shock_map.keys())

        return PredictionResponse(
            price_impacts={
                "oil": f"{round(oil, 2)}%",
                "gas": f"{round(gas, 2)}%"
            },
            shipping_delay_weeks=int(max(0, delay)),
            affected_industries=affected_regions,
            risk_severity=_map_risk(event.severity)
        )

    except Exception as e:
        print("ML failed, fallback to rule-based:", e)
        return _rule_based_fallback(event)


# --- Helper Functions ---

def _map_risk(severity: float) -> str:
    if severity > 0.7:
        return "High"
    elif severity > 0.4:
        return "Medium"
    return "Low"


def _rule_based_fallback(event: EventInput) -> PredictionResponse:
    # simplified fallback
    return PredictionResponse(
        price_impacts={"general": "+5%"},
        shipping_delay_weeks=1,
        affected_industries=[event.sector.value],
        risk_severity=_map_risk(event.severity)
    )