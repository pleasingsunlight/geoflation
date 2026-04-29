from fastapi import APIRouter
from backend.models.schemas import EventInput, PredictionResponse
from backend.services.prediction_service import predict_event_impact

router = APIRouter()


@router.post("/predict-event-impact", response_model=PredictionResponse)
def predict(event: EventInput):
    return predict_event_impact(event)