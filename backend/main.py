from fastapi import FastAPI
from backend.api.health import router as health_router
from backend.api.predict import router as predict_router
from backend.api.trade_network import router as trade_router

app = FastAPI(
    title="Geoflation API",
    description="Geopolitical Trade Shock Prediction System",
    version="0.1.0"
)

app.include_router(health_router)
app.include_router(predict_router)
app.include_router(trade_router)


@app.get("/")
def root():
    return {"message": "Geoflation API is running"}