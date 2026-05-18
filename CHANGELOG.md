# Changelog

## v1.1.0

Major backend and infrastructure upgrade introducing real datasets, improved forecasting, deployment support, and enhanced analytics.

### Added

- Real commodity price dataset integration
- Real trade network dataset support
- Affected countries prediction support
- Railway deployment configuration
- Commodity trend forecasting endpoint improvements
- Enhanced trade network API responses
- Frontend support for impacted countries display
- Improved caching for trade and commodity services

### Improved

- Backend modularity and service structure
- API response consistency
- Docker deployment workflow
- Frontend dashboard data rendering
- Prediction analysis explanations
- Error handling for missing datasets

### Infrastructure

- Railway production deployment support
- Docker deployment fixes for data pipelines
- Updated `.gitignore` strategy for dataset tracking
- Improved container compatibility for production builds

### Known Limitations

- Forecasting models are still lightweight/baseline
- Trade simulation still uses simplified propagation logic
- No GNN-based modeling yet
- No authentication or user accounts yet

---

## v1.0.0

Initial production release of Geoflation.

### Features

- Event impact prediction API (FastAPI)
- Graph-based trade shock propagation
- Commodity price forecasting (time-series)
- Strategic explanation layer
- Prediction history storage (PostgreSQL)
- Redis caching for performance
- Interactive frontend dashboard (Next.js)

### Infrastructure

- Full Dockerized stack (backend, frontend, DB, Redis)
- Environment-based configuration
- Modular backend architecture

### Limitations

- Uses synthetic/mock data
- ML models are basic (no GNN yet)
- No authentication
- No real-world deployment yet
