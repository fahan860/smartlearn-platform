# SmartLearn Platform

A full-stack personalized learning platform that combines a TypeScript REST API, a React web interface, a Python ML inference service, a synthetic data simulator, and a Spark/Pandas ETL pipeline — all orchestrated with Docker Compose.

> **Demo credentials** (after `docker-compose up --build`): `demo@example.com` / `Password123!`

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Data Pipeline](#data-pipeline)
- [ML Recommendation Service](#ml-recommendation-service)
- [Running Tests](#running-tests)
- [Known Limitations](#known-limitations)

---

## Overview

Generic learning platforms show the same catalogue to every user. SmartLearn tracks what each learner views, enrols in, and completes, then uses a recommendation engine (ML microservice with popularity fallback) to surface the most relevant next courses — giving each user a personalised feed.

**What the platform does:**

- JWT-secured authentication (signup, login, protected routes)
- Course catalogue with full-text search and filters (level, tag, keyword)
- Interaction tracking: `view`, `enroll`, `complete` events per user
- Personalised recommendations via ML service (sentence-transformer embeddings + cosine similarity), with cold-start fallback to popularity ranking
- Dual-database architecture: MongoDB for documents and interactions, MySQL for structured relational data
- Synthetic data pipeline: generates 1 200 users, 150 courses, 15 000 interactions for development and ML training
- Spark / Pandas ETL: normalises simulator output and loads into MySQL operational tables
- Fully containerised: one command starts all five services

---

## Architecture

```
┌─────────────┐        ┌──────────────────────┐        ┌─────────────────┐
│  React SPA  │◄──────►│  Backend (Node/TS)   │◄──────►│  ML Service     │
│  Port 80    │  REST  │  Port 4000           │  HTTP  │  (FastAPI/Py)   │
└─────────────┘        └──────────┬───────────┘        │  Port 8001      │
                                  │                     └────────┬────────┘
                          ┌───────┴───────┐                     │
                          │               │                      │
                   ┌──────▼─────┐  ┌──────▼──────┐             │
                   │  MongoDB 7 │  │  MySQL 8    │             │
                   │  Port 27017│  │  Port 3307  │◄────────────┘
                   └──────▲─────┘  └─────────────┘
                          │              ▲
                   ┌──────┴─────┐  ┌─────┴────────────────┐
                   │ Simulator  │  │  Spark / Pandas ETL   │
                   │ (Python)   │  │  feature_engineering  │
                   └────────────┘  └──────────────────────┘
```

**Request flow for recommendations:**

1. Frontend calls `GET /api/recommendations` with JWT
2. Backend fetches user's last 300 interactions → builds exclusion list
3. Backend gathers up to 1 000 candidate courses not yet seen
4. Backend calls ML service `POST /recommend` (2 s timeout)
5. ML service encodes course texts with `all-MiniLM-L6-v2`, builds user profile as mean of interaction embeddings, ranks by cosine similarity
6. On ML timeout/error → fallback to popularity ranking (interaction count)
7. Ordered course documents returned to frontend

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, Framer Motion, Axios |
| Backend API | Node.js 18, TypeScript, Express, Mongoose, JWT, express-validator |
| ML Service | Python 3.10+, FastAPI, Pydantic, sentence-transformers, NumPy, PyMongo |
| Data Simulator | Python, Faker, tqdm |
| ETL Pipeline | Apache Spark 3.5 (PySpark) / Pandas fallback |
| Databases | MongoDB 7, MySQL 8.4 |
| Infrastructure | Docker, Docker Compose, Nginx |
| Testing | Jest, MongoMemoryServer, supertest |

---

## Project Structure

```
smartlearn-platform/
├── backend/                        # REST API (TypeScript / Express)
│   ├── src/
│   │   ├── controllers/            # authController, courseController,
│   │   │                           # enrollmentController, interactionController,
│   │   │                           # recommendController
│   │   ├── middleware/             # JWT auth, errorHandler, validateRequest
│   │   ├── models/                 # Mongoose: User, Course, Interaction, LearningPath
│   │   ├── routes/                 # auth, courses, enrollments, interactions, recommendations
│   │   ├── scripts/seed.ts         # Demo data seeder
│   │   ├── services/
│   │   │   ├── mysql.service.ts    # mysql2/promise connection pool
│   │   │   └── recommendationService.ts  # ML call + popularity fallback
│   │   └── utils/httpError.ts
│   └── tests/                      # Jest: auth, courses, enrollments, recommendations
│
├── frontend/                       # Web UI (React / Vite)
│   └── src/
│       ├── components/             # CourseCard, Layout, ProtectedRoute
│       ├── contexts/AuthContext.tsx # JWT state management
│       ├── pages/                  # Landing, Login, Signup, Dashboard,
│       │                           # Courses, CourseDetail, Recommendations
│       └── services/api.ts         # Axios client for all API calls
│
├── ml-service/                     # Recommendation inference (FastAPI)
│   ├── main.py                     # Uvicorn entrypoint (used by Docker)
│   ├── config.py                   # Settings dataclass
│   ├── app/                        # Lightweight standalone version (not used by Docker)
│   └── src/ml_service/             # Active Docker runtime
│       ├── core/config.py          # Settings (MONGODB_URI, MODEL_PATH, port)
│       ├── data/processing.py      # build_candidate_pool()
│       ├── db/                     # mongo_client (singleton), repository
│       ├── models/schemas.py       # Pydantic: RecommendRequest / RecommendResponse
│       └── services/
│           ├── embedding_recommender.py  # sentence-transformers + cosine similarity
│           └── model_service.py          # ModelRegistry: .pkl loader + SHA-256 mock fallback
│
├── simulator/                      # Synthetic data generation
│   ├── src/data_generator.py       # Generates users, courses, interactions
│   ├── scripts/import_to_mongodb.py
│   └── config/config.yaml          # 1 200 users, 150 courses, 15 000 interactions
│
├── spark/                          # ETL pipeline
│   ├── jobs/
│   │   ├── feature_engineering.py         # PySpark canonical entity preparation
│   │   ├── feature_engineering_pandas.py  # Shim → delegates to run_feature_engineering
│   │   ├── run_feature_engineering.py     # Pandas fallback (recommended on Windows)
│   │   └── load_to_mysql.py               # Loads processed CSVs into MySQL
│   ├── run_pipeline.py             # Orchestrator: Spark → MySQL
│   └── config/spark.conf
│
├── database/mysql/
│   ├── schema.sql                  # Tables: users, courses, enrollments, interactions
│   └── seed.sql                    # 3 demo users, 3 courses, 5 enrollments, 12 interactions
│
├── docs/
│   ├── SETUP.md
│   ├── FEATURES.md
│   ├── docker.md
│   ├── MySQL.md
│   └── QUICKREF.md
│
├── notebooks/                      # Exploratory analysis
├── docker-compose.yml              # 5-service orchestration
├── .env.example                    # All environment variables documented
├── config.py                       # Root path constants (Python)
└── main.py                         # Informational entrypoint
```

---

## Quick Start

### Option A — Docker (recommended)

```bash
git clone https://github.com/your-username/smartlearn-platform.git
cd smartlearn-platform
cp .env.example .env          # review and adjust secrets
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost |
| Backend API | http://localhost:4000 |
| ML Service | http://localhost:8001 |
| MySQL | localhost:3307 |
| MongoDB | localhost:27017 |

MySQL auto-initialises with `schema.sql` and `seed.sql` on first run.
Demo credentials: `demo@example.com` / `Password123!`

---

### Option B — Local development

**Prerequisites:** Node.js 18+, Python 3.10+, MongoDB 7, MySQL 8

```bash
# 1. Backend
cd backend
cp ../.env.example .env       # set MONGODB_URI, JWT_SECRET, MYSQL_*
npm install
npm run dev                   # http://localhost:4000

# Seed demo data (optional)
npm run seed

# 2. Frontend (new terminal)
cd frontend
npm install
npm run dev                   # http://localhost:5173

# 3. ML Service (new terminal)
cd ml-service
pip install -r requirements.txt
python main.py                # http://localhost:8001
```

---

### Option C — Generate synthetic data & populate MongoDB

```bash
# Step 1 — generate data
cd simulator/src
python data_generator.py
# Output: simulator/src/data/raw/{users,courses,interactions}/

# Step 2 — import into MongoDB
cd ../scripts
python import_to_mongodb.py \
  --data-dir ../src/data/raw \
  --db-name learning \
  --db-uri mongodb://localhost:27017

# Step 3 — run ETL into MySQL (Pandas, no Spark install required)
cd ../../spark
python jobs/feature_engineering_pandas.py   # → data/processed/
python jobs/load_to_mysql.py \
  --host localhost --port 3307 \
  --user smartlearn --password smartlearn_password \
  --database smartlearn \
  --data-path data/processed
```

> **Note on Spark (Windows):** PySpark requires `winutils.exe` on Windows. The Pandas fallback (`feature_engineering_pandas.py`) produces identical output without this dependency and is recommended for local development.

---

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `NODE_ENV` | `development` | Backend Node environment |
| `PORT` | `4000` | Backend HTTP port |
| `MONGODB_URI` | `mongodb://127.0.0.1:27017/smartlearn` | MongoDB connection string |
| `JWT_SECRET` | *(required)* | JWT signing secret — change in production |
| `MYSQL_HOST` | `localhost` | MySQL host |
| `MYSQL_PORT` | `3306` | MySQL port (`3307` when using Docker from host) |
| `MYSQL_DATABASE` | `smartlearn` | MySQL database name |
| `MYSQL_USER` | `root` | MySQL user |
| `MYSQL_PASSWORD` | `root` | MySQL password |
| `ML_SERVICE_URL` | `http://localhost:8001` | ML service base URL (fallback used if unreachable) |
| `VITE_API_BASE_URL` | `http://localhost:4000` | Frontend API base URL |
| `MODEL_PATH` | `/app/models/recommender.pkl` | Path to trained recommender model (optional) |

---

## API Reference

All protected routes require `Authorization: Bearer <token>`.

### Auth

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/api/auth/signup` | — | Create account, returns JWT |
| `POST` | `/api/auth/login` | — | Login, returns JWT |
| `GET` | `/api/auth/me` | ✓ | Returns `{ _id, name, email, createdAt }` |

### Courses

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/api/courses` | — | List courses (`?q=&level=&tag=`), limit 100 |
| `GET` | `/api/courses/:id` | — | Get single course by MongoDB ObjectId |
| `POST` | `/api/courses` | ✓ | Create course (title, description, tags, level, durationMinutes) |
| `GET` | `/api/courses/mysql` | — | List courses from MySQL (id, title, description, level) |

### Interactions

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/api/interactions/record` | ✓ | Record `view` / `enroll` / `complete` |
| `GET` | `/api/interactions/me` | ✓ | User's last 200 interactions |

### Enrollments

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/api/enrollments` | ✓ | Enrol in a course (idempotent) |

### Recommendations

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/api/recommendations` | ✓ | Personalised course list (ML or popularity fallback) |

### Health

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Backend status |
| `GET` | `http://localhost:8001/health` | ML service status |

---

## Data Pipeline

```
simulator/src/data_generator.py
        │  generates (JSON + CSV)
        ▼
simulator/src/data/raw/
  ├── users/          1 200 users
  ├── courses/        150 courses (6 categories, 3 levels)
  └── interactions/   15 000 events (view, enroll, progress, complete)
        │
        ├──► import_to_mongodb.py ──► MongoDB (learning db)
        │                              used directly by backend & ML service
        │
        └──► feature_engineering_pandas.py (or PySpark version)
                      │  normalises & transforms
                      ▼
              spark/data/processed/
                ├── users/
                ├── courses/
                ├── enrollments/    (derived from interactions)
                └── interactions/   (filtered to view|enroll|complete)
                      │
                      └──► load_to_mysql.py ──► MySQL (smartlearn db)
```

**Key transformation** — the simulator generates interaction types `view`, `enroll`, `progress`, `complete`. The ETL pipeline remaps `enrollment→enroll`, `completion→complete`, and drops `progress` to match the MySQL schema ENUM.

**Enrollment derivation** — the MySQL `enrollments` table does not exist in MongoDB; it is computed by the ETL by grouping interactions: `enrolled_at = min(enroll/complete timestamp)`, `completed_at = max(complete timestamp)`.

---

## ML Recommendation Service

The ML service exposes `POST /recommend` and is called by the backend with a 2-second timeout. Two implementations coexist:

**Active (Docker runtime)** — `src/ml_service/` via `main.py` launcher:
- Loads `all-MiniLM-L6-v2` (sentence-transformers) to encode course text (`title + description + level + tags`)
- Builds a user profile as the **mean embedding** of the user's last 20 interacted courses (fetched from MongoDB)
- Ranks candidates by **cosine similarity** between each candidate and the user profile
- **Cold start** (no interaction history): returns candidates in input order; backend fallback handles popularity ranking

**Model file (optional)** — if `/app/models/recommender.pkl` exists and exposes a `.predict(user_id, candidate_ids)` method, `ModelRegistry` loads it instead of the embedding approach.

**Mock fallback** — if no `.pkl` is found, a deterministic SHA-256 hash of `user_id:course_id` is used to produce stable (but non-personalised) scores. This ensures the service never returns an error even without a trained model.

**Backend fallback** — if the ML service times out or errors, `recommendationService.ts` falls back to popularity ranking: courses sorted by total interaction count descending.

---

## Running Tests

```bash
cd backend
npm test
```

Tests use `MongoMemoryServer` (in-memory MongoDB) and `supertest`. Coverage:

- `auth.test.ts` — signup and login (JWT returned, validation errors)
- `courses.test.ts` — list courses, level filter
- `enrollments.test.ts` — auth required (401), idempotent enrolment (201 first, 200 repeat)
- `recommendations.test.ts` — auth required (401), mocked recommendations array

---

## Known Limitations

- **Simulator user passwords** are stored as plaintext strings in MongoDB (`"password": "abc123"`). The backend expects bcrypt hashes. Users generated by the simulator cannot log in without running a password re-hashing script.
- **Simulator course IDs** use the format `"course_NNNNN"` which is not a valid MongoDB ObjectId. `GET /api/courses/:id` will throw a cast error for these courses. Re-import without `_id` to let MongoDB generate proper ObjectIds.
- **Spark on Windows** requires `winutils.exe` and `HADOOP_HOME`. Use `feature_engineering_pandas.py` instead — it produces identical output.
- **ML personalisation** requires at least one interaction in MongoDB for a user. New users see popularity-ranked courses until they interact with the platform.
- **ML service timeout** is set to 2 000 ms in `recommendationService.ts`. The `all-MiniLM-L6-v2` model may exceed this on first load. Increase to 5 000 ms if recommendations always fall back to popularity.

---

## Future Improvements

- Collaborative filtering model trained on simulated interaction dataset
- Progress tracking and completion certificates
- Admin dashboard for course management
- OAuth2 social login (Google / GitHub)
- Real-time notification feed (WebSocket)
- Airflow DAG for automated ETL scheduling
- Password re-hashing utility for simulator-generated users
