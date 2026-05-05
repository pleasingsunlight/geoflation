from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.health import router as health_router
from backend.api.predict import router as predict_router
from backend.api.trade_network import router as trade_router
from backend.api.commodities import router as commodities_router
from backend.config import engine
from backend.models.db_models import Base

app = FastAPI(
    title="Geoflation API",
    description="Geopolitical Trade Shock Prediction System",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

# CORS CONFIG 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(predict_router)
app.include_router(trade_router)
app.include_router(commodities_router)


@app.get("/")
def root():
    return {"message": "Geoflation API is running"}