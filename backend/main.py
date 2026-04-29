from fastapi import FastAPI
from backend.api.health import router as health_router

app = FastAPI(
    title="Geoflation API",
    description="Geopolitical Trade Shock Prediction System",
    version="0.1.0"
)

# Register routes
app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "Geoflation API is running"}