from backend.models.schemas import EventInput, PredictionResponse


def predict_event_impact(event: EventInput) -> PredictionResponse:
    """
    Placeholder logic (will be replaced with rule engine in next step)
    """

    return PredictionResponse(
        price_impacts={"oil": "0%", "gas": "0%"},
        shipping_delay_weeks=0,
        affected_industries=[],
        risk_severity="Low"
    )