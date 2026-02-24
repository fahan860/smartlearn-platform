# SmartLearn Platform

## Problem
Modern learning platforms often struggle to provide personalized course recommendations, maintain consistent data pipelines, and operate reliably across backend, frontend, and ML services in production.

## Solution
SmartLearn is organized as a production-oriented monorepo combining:
- a TypeScript backend API
- a React frontend
- a Python ML inference service
- data engineering and simulation pipelines for feature generation

The repository is structured to separate responsibilities clearly (API, UI, ML inference, data processing, infrastructure, and documentation), improving maintainability and onboarding.

## Tech Stack
- **Backend:** Node.js, TypeScript, Express, Jest
- **Frontend:** React, TypeScript, Vite, Tailwind CSS
- **ML Service:** Python, FastAPI, Uvicorn, Pydantic
- **Data/ML Pipelines:** Python, Pandas, Spark
- **Databases:** MySQL, MongoDB
- **Infra:** Docker, Docker Compose

## Architecture
```text
.
├── backend/                # REST API (TypeScript)
├── frontend/               # Web application (React)
├── ml-service/             # ML inference service (FastAPI)
│   ├── src/ml_service/
│   │   ├── core/           # Configuration
│   │   ├── data/           # Data processing logic
│   │   ├── db/             # Persistence abstractions
│   │   ├── models/         # Pydantic schemas
│   │   └── services/       # Model inference logic
│   ├── models/             # Trained model artifacts
│   └── main.py             # Service entry point
├── simulator/              # Data simulation scripts
├── spark/                  # Feature engineering pipelines
├── data/                   # Raw, processed, generated data
├── database/               # SQL schemas and seeds
├── docs/                   # Project documentation
├── notebooks/              # Exploratory analysis notebooks
├── screenshots/            # Demo screenshots for README/docs
└── docker-compose.yml      # Local orchestration
```

## Results
- Clear service boundaries and domain separation for ML components
- `src/`-based Python package layout in the ML service
- Root-level GitHub essentials (`README.md`, `.gitignore`, `requirements.txt`)
- Dedicated folders for notebooks, screenshots, and model artifacts
- Improved developer onboarding and production-readiness without changing core behavior

## Quick Start
1. Start all services:
   ```bash
   docker-compose up --build
   ```
2. ML service health:
   ```bash
   http://localhost:8001/health
   ```
3. Backend health:
   ```bash
   http://localhost:4000/health
   ```
