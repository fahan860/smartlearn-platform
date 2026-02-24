import logging
import os
from fastapi import FastAPI, HTTPException

from .model_service import ModelRegistry
from .schemas import RecommendRequest, RecommendResponse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ml-service")

app = FastAPI(title="SmartLearn ML Recommender", version="1.0.0")
registry = ModelRegistry(model_path=os.getenv("MODEL_PATH"))


@app.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(payload: RecommendRequest) -> RecommendResponse:
	try:
		excluded = set(payload.excludeCourseIds)
		candidates = [course_id for course_id in payload.candidateCourseIds if course_id not in excluded]

		if not candidates:
			return RecommendResponse(courseIds=[])

		ranked = registry.recommend(
			user_id=payload.userId,
			candidates=candidates,
			top_k=payload.topK,
		)

		return RecommendResponse(courseIds=ranked)
	except Exception as error:
		logger.exception("Recommendation inference failed: %s", error)
		raise HTTPException(status_code=500, detail="Inference failed") from error
