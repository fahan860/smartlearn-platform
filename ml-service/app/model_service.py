import hashlib
import logging
import os
import pickle
from dataclasses import dataclass
from typing import Callable, List


logger = logging.getLogger(__name__)


def _stable_score(user_id: str, course_id: str) -> float:
	raw = f"{user_id}:{course_id}".encode("utf-8")
	digest = hashlib.sha256(raw).hexdigest()
	return int(digest[:12], 16) / float(16**12)


@dataclass
class InferenceModel:
	predict_fn: Callable[[str, List[str]], List[str]]

	def recommend(self, user_id: str, candidates: List[str], top_k: int) -> List[str]:
		ranked = self.predict_fn(user_id, candidates)
		return ranked[:top_k]


class ModelRegistry:
	def __init__(self, model_path: str | None = None):
		self.model_path = model_path or os.getenv("MODEL_PATH", "/app/models/recommender.pkl")
		self._model = self._load_model()

	def _load_model(self) -> InferenceModel:
		if os.path.exists(self.model_path):
			try:
				with open(self.model_path, "rb") as model_file:
					loaded = pickle.load(model_file)

				if hasattr(loaded, "predict"):
					logger.info("Loaded trained model from %s", self.model_path)

					def _predict(user_id: str, candidates: List[str]) -> List[str]:
						scores = loaded.predict(user_id=user_id, candidate_ids=candidates)
						scored = sorted(scores.items(), key=lambda item: item[1], reverse=True)
						return [course_id for course_id, _ in scored]

					return InferenceModel(predict_fn=_predict)
			except Exception as error:
				logger.exception("Failed to load trained model at %s: %s", self.model_path, error)

		logger.warning("No trained model found. Using deterministic mock model.")

		def _mock_predict(user_id: str, candidates: List[str]) -> List[str]:
			scored = sorted(candidates, key=lambda cid: _stable_score(user_id, cid), reverse=True)
			return scored

		return InferenceModel(predict_fn=_mock_predict)

	def recommend(self, user_id: str, candidates: List[str], top_k: int) -> List[str]:
		return self._model.recommend(user_id=user_id, candidates=candidates, top_k=top_k)
