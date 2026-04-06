import logging

from fastapi import FastAPI, HTTPException

from ml_service.core.config import settings
from ml_service.data.processing import build_candidate_pool
from ml_service.db.mongo_client import get_db
from ml_service.db.repository import RecommendationRepository
from ml_service.models.schemas import RecommendRequest, RecommendResponse
from ml_service.services.embedding_recommender import EmbeddingRecommender
from ml_service.services.model_service import ModelRegistry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ml-service")

app = FastAPI(title=settings.app_name, version=settings.app_version)
registry = ModelRegistry(model_path=settings.model_path)
repository = RecommendationRepository()

db = get_db()
embedding_recommender = EmbeddingRecommender(db=db)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(payload: RecommendRequest) -> RecommendResponse:
    try:
        candidates = build_candidate_pool(payload)

        # Apply exclusions + de-duplicate while preserving order
        excludes = set(payload.excludeCourseIds or [])
        seen: set[str] = set()
        candidates = [
            cid for cid in candidates
            if cid not in excludes and not (cid in seen or seen.add(cid))
        ]

        if not candidates:
            return RecommendResponse(courseIds=[])

        ranked = embedding_recommender.recommend(
            user_id=payload.userId,
            candidate_course_ids=candidates,
            top_k=payload.topK,
        )

        repository.save_recommendation_event(
            user_id=payload.userId,
            selected_course_ids=ranked,
        )
        return RecommendResponse(courseIds=ranked)
    except Exception as error:
        logger.exception("Recommendation inference failed: %s", error)
        raise HTTPException(status_code=500, detail="Inference failed") from error