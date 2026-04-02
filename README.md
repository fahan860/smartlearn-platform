# SmartLearn Platform

A full-stack personalized learning platform that combines a TypeScript REST API, a React web interface, and a Python ML inference service to deliver course recommendations tailored to each learner's behaviour.

## Problem → Solution

Generic learning platforms show the same catalogue to every user. SmartLearn tracks what each learner views, enrols in, and completes, then uses a lightweight recommendation engine (with an ML microservice fallback) to surface the most relevant next courses — giving each user a personalised feed from their very first interaction.

## Key Features

- **JWT-secured authentication** — sign-up, login, and protected routes
- **Course catalogue** — search and filter by level, tag, or keyword
- **Interaction tracking** — records view / enrol / complete events per user
- **Personalised recommendations** — tag-affinity scoring with recency decay; cold-start falls back to popular courses; optional ML microservice via FastAPI
- **Dual-database architecture** — MongoDB for documents and interactions, MySQL for structured relational data
- **Data pipeline** — Spark feature-engineering jobs and a simulation layer for generating realistic training data
- **Fully containerised** — single `docker-compose up --build` starts all five services

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, Framer Motion |
| Backend API | Node.js, TypeScript, Express, Mongoose, JWT |
| ML Service | Python, FastAPI, Pydantic, scikit-learn |
| Data Pipelines | Apache Spark, Pandas |
| Databases | MongoDB 7, MySQL 8 |
| Infrastructure | Docker, Docker Compose, Nginx |

## Project Structure

```
smartlearn-platform/
├── backend/            # REST API (TypeScript / Express)
│   ├── src/
│   │   ├── controllers/   # Route handlers
│   │   ├── middleware/    # Auth, validation, error handling
│   │   ├── models/        # Mongoose schemas
│   │   ├── routes/        # Express routers
│   │   ├── services/      # Business logic (ML, MySQL)
│   │   └── utils/
│   └── tests/             # Jest test suite
├── frontend/           # Web UI (React / Vite)
│   └── src/
│       ├── components/    # Reusable UI components
│       ├── contexts/      # Auth context
│       ├── pages/         # Route-level page components
│       └── services/      # Axios API client
├── ml-service/         # Recommendation inference (FastAPI)
│   └── src/ml_service/
│       ├── core/          # Configuration
│       ├── data/          # Data processing
│       ├── db/            # Persistence abstractions
│       ├── models/        # Pydantic schemas
│       └── services/      # Model inference
├── simulator/          # Synthetic data generation
├── spark/              # Feature engineering pipelines
├── database/           # MySQL schema + seed SQL
├── docs/               # Setup, quick-reference, and technical guides
├── notebooks/          # Exploratory analysis
└── docker-compose.yml  # Full-stack orchestration
```

## Quick Start

### Option A — Docker (recommended)

```bash
cp .env.docker.example .env
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost |
| Backend API | http://localhost:4000 |
| ML Service | http://localhost:8001 |

### Option B — Local development

**Prerequisites:** Node.js 18+, MongoDB, MySQL 8, Python 3.10+

```bash
# Backend
cd backend
cp .env.example .env          # fill in MONGODB_URI, JWT_SECRET, MYSQL_*
npm install
npm run dev                   # http://localhost:4000

# Frontend (separate terminal)
cd frontend
cp .env.example .env
npm install
npm run dev                   # http://localhost:3000

# Seed demo data (optional)
cd backend && npm run seed
```

Demo credentials (after seeding): `demo@example.com` / `Password123!`

## API Overview

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/signup` | — | Create account |
| POST | `/api/auth/login` | — | Return JWT |
| GET | `/api/courses` | — | List courses (`?q=&level=&tag=`) |
| GET | `/api/recommendations` | ✓ | Personalised recommendations |
| POST | `/api/interactions/record` | ✓ | Log view / enrol / complete |
| GET | `/api/interactions/me` | ✓ | User's interaction history |

Full API docs: [`backend/README.md`](backend/README.md)

## Running Tests

```bash
cd backend
npm test          # Jest — runs against an in-memory MongoDB instance
```

## Future Improvements

- Collaborative filtering model trained on the simulated interaction dataset
- Progress tracking and completion certificates
- Admin dashboard for course management
- OAuth2 social login (Google / GitHub)
- Real-time notification feed (WebSocket)
