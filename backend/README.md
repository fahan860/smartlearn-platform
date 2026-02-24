# Backend - Learning Recommender

Express + TypeScript API that handles auth, catalog, user interactions, and personalized course recommendations.

## Setup

1. Copy `.env.example` to `.env` and fill values (MongoDB Atlas URI, JWT secret, optional ML service URL).
2. Install dependencies: `npm install`
3. Run dev server: `npm run dev`
4. Run tests (uses in-memory MongoDB): `npm test`

## Scripts
- `npm run dev` – ts-node-dev with reload
- `npm run build` – compile TypeScript to `dist/`
- `npm start` – run compiled server
- `npm run seed` – seed demo data into the configured MongoDB

## API quick reference
- `POST /api/auth/signup` – create account `{ name, email, password }`
- `POST /api/auth/login` – returns JWT
- `GET /api/courses` – list courses with optional `?tag=&level=&q=` filters
- `POST /api/courses` – create course (auth required)
- `POST /api/interactions/record` – log user interaction `{ course, action, progress?, metadata? }`
- `GET /api/interactions/me` – recent interactions
- `GET /api/recommendations` – personalized recommendations for the authenticated user

## Recommendation logic
- Tries an optional ML microservice if `ML_SERVICE_URL` is set (POST `/recommend` with user + interaction IDs).
- Fallback: ranks tags from recent interactions with action weights and light recency decay, then returns similar courses; cold-start returns recent courses.

## Docker
Multi-stage build installs dev deps for TypeScript compile, then runs with production-only deps:

```bash
docker build -t learning-recommender .
docker run -p 4000:4000 --env-file .env learning-recommender
```

## Notes
- MongoDB defaults to local `mongodb://127.0.0.1:27017/learning` in non-production if env vars are missing.
- Emails are normalized (lowercase/trim). Request validation is enforced via `express-validator` + middleware.
