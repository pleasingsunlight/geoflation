def generate_explanation(event, shock_map, price_impacts, delay):
    country = event.country
    event_type = event.event_type.value
    sector = event.sector.value
    severity = event.severity

    impacted = ", ".join(shock_map.keys())

    explanation = f"""
A {event_type} event in {country} affecting the {sector} sector with severity {severity}
is expected to disrupt global trade flows.

Primary impact originates in {country}, with ripple effects observed in {impacted}.

Commodity markets respond with changes such as {price_impacts}, while
logistics disruptions may cause approximately {delay} weeks of delay.

Overall, this event poses a {('high' if severity > 0.7 else 'moderate' if severity > 0.4 else 'low')}
risk to global supply chains.
"""

    return explanation.strip()