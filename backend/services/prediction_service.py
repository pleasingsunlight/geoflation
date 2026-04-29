from backend.models.schemas import EventInput, PredictionResponse


def predict_event_impact(event: EventInput) -> PredictionResponse:
    price_impacts = {}
    shipping_delay = 0
    affected_industries = set()

    severity = event.severity

    # --- RULE 1: Sanctions ---
    if event.event_type.value == "sanction":
        if event.sector.value == "energy":
            price_impacts["oil"] = f"+{int(10 * severity)}%"
            price_impacts["gas"] = f"+{int(8 * severity)}%"
            affected_industries.update(["energy", "transport"])

        elif event.sector.value == "technology":
            price_impacts["semiconductors"] = f"+{int(12 * severity)}%"
            affected_industries.update(["electronics", "automotive"])

    # --- RULE 2: War ---
    elif event.event_type.value == "war":
        shipping_delay += int(2 * severity)
        price_impacts["oil"] = f"+{int(15 * severity)}%"
        affected_industries.update(["energy", "logistics", "defense"])

    # --- RULE 3: Tariffs ---
    elif event.event_type.value == "tariff":
        price_impacts["manufacturing"] = f"+{int(5 * severity)}%"
        affected_industries.update(["manufacturing", "retail"])

    # --- RULE 4: Port Closure ---
    elif event.event_type.value == "port_closure":
        shipping_delay += int(3 * severity)
        affected_industries.update(["logistics", "global_trade"])

    # --- DEFAULT RULE ---
    if not price_impacts:
        price_impacts["general"] = f"+{int(3 * severity)}%"

    # --- RISK SEVERITY ---
    if severity > 0.7:
        risk = "High"
    elif severity > 0.4:
        risk = "Medium"
    else:
        risk = "Low"

    return PredictionResponse(
        price_impacts=price_impacts,
        shipping_delay_weeks=shipping_delay,
        affected_industries=list(affected_industries),
        risk_severity=risk
    )