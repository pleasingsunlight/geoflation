from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.health import router as health_router
from backend.api.predict import router as predict_router
from backend.api.trade_network import router as trade_router
from backend.api.commodities import router as commodities_router
from backend.config import engine
from backend.models.db_models import Base
from backend.api.history import router as history_router

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
app.include_router(history_router)


@app.get("/")
def root():
    return {"message": "Geoflation API is running"}


import os

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port
    )