from backend.models.schemas import EventInput, PredictionResponse
from backend.ml_models.model_loader import get_model
from backend.data_pipeline.feature_engineering import build_features_from_event
from backend.services.explanation_service import generate_explanation
from backend.config import SessionLocal
from backend.models.db_models import Prediction
from backend.ml_models.trade_propagation import (
    propagate_trade_shock
)


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

        impacted_countries = propagate_trade_shock(
            source_country=event.country,
            severity=event.severity
        )

        affected_industries = [event.sector.value]

        explanation = generate_explanation(
            event,
            impacted_countries,
            {
                "oil": round(float(oil), 2),
                "gas": round(float(gas), 2)
            },
            int(max(0, delay))
        )

        db = SessionLocal()

        db_pred = Prediction(
            event_type=event.event_type.value,
            country=event.country,
            sector=event.sector.value,
            severity=event.severity,
            oil_impact=f"{round(oil, 2)}%",
            gas_impact=f"{round(gas, 2)}%",
            delay=int(max(0, delay)),
            risk=_map_risk(event.severity)
        )

        db.add(db_pred)
        db.commit()
        db.close()
        
        return PredictionResponse(
            price_impacts={
                "oil": f"{round(oil, 2)}%",
                "gas": f"{round(gas, 2)}%"
            },
            shipping_delay_weeks=int(max(0, delay)),
            impacted_countries=impacted_countries,
            affected_industries=affected_industries,
            risk_severity=_map_risk(event.severity),
            explanation=explanation
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
        impacted_countries={
            event.country: round(event.severity, 2)
        },
        affected_industries=[event.sector.value],
        risk_severity=_map_risk(event.severity),
        explanation="Fallback rule-based prediction due to ML failure."
    )