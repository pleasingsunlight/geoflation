# Geoflation

Geoflation is an end-to-end geopolitical trade shock prediction platform with a dashboard frontend and a FastAPI backend.

It analyzes geopolitical events (sanctions, wars, tariffs, embargoes, naval blockades, port disruptions, etc.) and predicts their impact on global trade flows, supply chains, shipping networks, and commodity markets.

The platform combines:
- real commodity forecasting
- trade network graph propagation
- ML-driven prediction pipelines
- geopolitical risk simulation
- production-grade infrastructure

---

## Version

Current version: v1.1.0

---

## Live Demo

Frontend: https://geoflation.vercel.app

Backend API Docs: https://geoflation-production.up.railway.app/docs

---

## What this project does

- Input a geopolitical event from the web dashboard
- Run event impact prediction using ML + rule-based fallback
- Forecast commodity price disruptions using real historical datasets
- Simulate weighted trade shock propagation across countries
- Model cascading multi-hop geopolitical disruptions
- Estimate shipping delays and risk severity
- Store predictions in PostgreSQL
- Cache expensive computations with Redis
- Display forecasts, trade graphs, and prediction history in a dashboard

---

## Architecture

```mermaid
graph TD

User[User Browser]
Frontend[Next.js Frontend]
Backend[FastAPI Backend]

API[API Layer]
Prediction[Prediction Service]

Graph[Trade Graph Propagation Engine]
Forecast[Commodity Forecast Engine]

TradeData[Trade Network Dataset]
CommodityData[Commodity Price Dataset]

DB[(PostgreSQL)]
Cache[(Redis)]

User --> Frontend
Frontend --> Backend

Backend --> API
API --> Prediction

Prediction --> Graph
Prediction --> Forecast

Graph --> TradeData
Forecast --> CommodityData

Prediction --> DB
Prediction --> Cache

Prediction --> Backend
Backend --> Frontend
```

---

## Deployment Architecture

```mermaid
graph TD

User[User Browser]

Vercel[Vercel Frontend]
Railway[Railway Backend]

Postgres[(PostgreSQL)]
Redis[(Redis)]

User --> Vercel
Vercel --> Railway

Railway --> Postgres
Railway --> Redis
```

---

## Runtime Request Flow

```mermaid
sequenceDiagram

participant User
participant Frontend
participant Backend
participant Cache
participant Forecast
participant Graph
participant DB

User->>Frontend: Submit geopolitical event

Frontend->>Backend: POST /predict-event-impact

Backend->>Cache: Check cache

alt Cache hit
    Cache-->>Backend: Cached response
else Cache miss

    Backend->>Forecast: Forecast commodity impacts
    Forecast-->>Backend: Oil/Gas/Wheat projections

    Backend->>Graph: Run propagation engine
    Graph-->>Backend: Cascading impacted countries

    Backend->>DB: Store prediction
end

Backend-->>Frontend: Prediction response

Frontend-->>User: Render dashboard + graphs
```

---

## Internal Pipeline Architecture

```mermaid
graph TD

API[FastAPI Endpoint /predict-event-impact]

Validation[Pydantic Validation Layer]

FeatureEng[Feature Engineering<br/>One-hot Encoding + Alignment]

FeatureStore[(Feature Schema / Cached Columns)]

ModelRouter[Model Router]

PriceModel[Commodity Impact Model]
DelayModel[Shipping Delay Model]

TradeGraph[Trade Network Propagation Engine]

ForecastEngine[Prophet Forecasting Engine]

CommodityData[(Historical Commodity Dataset)]

TradeDataset[(Trade Network Dataset)]

PostProcess[Business Logic Layer<br/>Risk Scoring + Aggregation]

Formatter[Response Builder]

DB[(PostgreSQL - Prediction History)]

Cache[(Redis / In-Memory Cache)]

API --> Validation
Validation --> FeatureEng
FeatureEng --> FeatureStore

FeatureEng --> ModelRouter

ModelRouter --> PriceModel
ModelRouter --> DelayModel

PriceModel --> ForecastEngine
ForecastEngine --> CommodityData

DelayModel --> PostProcess

TradeGraph --> TradeDataset
TradeGraph --> PostProcess

ForecastEngine --> PostProcess

PostProcess --> Formatter

Formatter --> DB
Formatter --> Cache

Formatter --> API
```

---

## Tech Stack

### Frontend

- Next.js
- TailwindCSS
- Recharts

### Backend

- FastAPI
- Python 3.11
- Uvicorn
- SQLAlchemy

### Machine Learning & Analytics

- Scikit-learn
- Prophet
- NetworkX
- Pandas
- NumPy

### Infrastructure

- Docker
- PostgreSQL
- Redis
- Railway
- Vercel

---

## Repository Structure

```text
geoflation/
├── backend/
│   ├── main.py
│   ├── api/
│   ├── ml_models/
│   │   ├── price_forecast.py
│   │   ├── trade_propagation.py
│   │   └── model_loader.py
│   ├── services/
│   ├── data_pipeline/
│   │   ├── preprocess_commodity_data.py
│   │   └── load_trade_network.py
│   ├── models/
│   ├── utils/
│   └── config.py
│
├── frontend/
│   ├── app/
│   ├── components/
│   └── styles/
│
├── data/
│   ├── raw/
│   │   ├── commodities/
|   |       └──commodity_prices_processed.csv
│   │   └── trade/
|   |       └──trade_edges.csv 
│   └── processed/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## API Overview

### GET /health

Returns backend health status.

---

### POST /predict-event-impact

Input:

```json
{
  "event_type": "war",
  "country": "Russia",
  "sector": "energy",
  "severity": 0.9
}
```

Output:

```json
{
  "price_impacts": {
    "oil": "17.41%",
    "gas": "13.07%"
  },
  "shipping_delay_weeks": 2,
  "impacted_countries": {
    "China": 0.72,
    "EU": 0.63,
    "USA": 0.48
  },
  "affected_industries": [
    "energy"
  ],
  "risk_severity": "High",
  "explanation": "..."
}
```

---

### GET /commodity-trends

Returns Prophet-generated commodity forecasting data using historical datasets.

---

### GET /trade-network

Returns weighted trade graph data used for geopolitical propagation.

---

### GET /prediction-history

Returns stored historical predictions from PostgreSQL.

---

## Real Data Sources

### Commodity Price Data

Source:
World Bank Pink Sheet Dataset

Integrated:
- crude oil
- natural gas
- wheat

Dataset frequency:
- monthly historical data
- 1960 → present

---

### Trade Network Data

Current version uses:
- curated weighted trade relationships
- NetworkX directed graph modeling

Foundation prepared for:
- UN Comtrade integration
- large-scale graph ingestion
- Graph Neural Networks

---

## Local Development

### 1) Full Stack (Docker)

```bash
docker-compose up --build
```

Frontend:
http://localhost:3000

Backend:
http://localhost:8000/docs

---

### 2) Backend (Manual)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

uvicorn backend.main:app --reload
```

---

### 3) Frontend (Manual)

```bash
cd frontend

npm install

npm run dev
```

---

## Deployment

| Service | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Railway |
| Database | PostgreSQL (Railway) |
| Cache | Redis (Railway) |

---

## Core Components

### Prediction Service

Handles geopolitical event → disruption prediction using ML models.

---

### Trade Graph Propagation Engine

Simulates weighted cascading trade disruptions across global trade networks.

Supports:
- multi-hop propagation
- severity decay
- graph traversal

---

### Commodity Forecasting Engine

Uses Prophet-based time-series forecasting on real historical commodity datasets.

Forecasted commodities:
- oil
- gas
- wheat

---

### Persistence Layer

Stores prediction history in PostgreSQL.

---

### Caching Layer

Uses Redis to cache:
- commodity forecasts
- trade network responses
- expensive graph computations

---

## Future Work

- Full UN Comtrade ingestion pipeline
- Graph centrality scoring
- Country vulnerability indices
- JWT authentication
- Graph Neural Networks (PyTorch Geometric)
- LLM-based strategic explanation layer
- Probabilistic geopolitical forecasting
- Maritime chokepoint disruption modeling

---

## License

MIT License
