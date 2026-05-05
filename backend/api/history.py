from fastapi import APIRouter
from backend.config import SessionLocal
from backend.models.db_models import Prediction

router = APIRouter()


@router.get("/prediction-history")
def get_prediction_history():
    db = SessionLocal()
    preds = db.query(Prediction).all()
    db.close()

    return [
        {
            "event_type": p.event_type,
            "country": p.country,
            "sector": p.sector,
            "severity": p.severity,
            "oil": p.oil_impact,
            "gas": p.gas_impact,
            "delay": p.delay,
            "risk": p.risk,
        }
        for p in preds
    ]