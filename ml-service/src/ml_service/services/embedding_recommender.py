from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

import numpy as np
from bson import ObjectId
from pymongo.database import Database
from sentence_transformers import SentenceTransformer


@dataclass(frozen=True)
class EmbeddingRecommender:
    db: Database
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    user_history_limit: int = 20

    def __post_init__(self) -> None:
        # Lazy-load is possible, but simple load is fine for a small service.
        object.__setattr__(self, "_model", SentenceTransformer(self.model_name))

    def recommend(self, user_id: str, candidate_course_ids: list[str], top_k: int) -> list[str]:
        if not candidate_course_ids:
            return []

        candidate_oids = [ObjectId(cid) for cid in candidate_course_ids if ObjectId.is_valid(cid)]
        if not candidate_oids:
            return []

        user_oid = ObjectId(user_id) if ObjectId.is_valid(user_id) else None

        # Fetch candidate course docs
        courses = list(
            self.db["courses"].find(
                {"_id": {"$in": candidate_oids}},
                {"title": 1, "description": 1, "tags": 1, "level": 1},
            )
        )
        if not courses:
            return []

        course_id_to_text: dict[str, str] = {}
        for c in courses:
            cid = str(c["_id"])
            title = (c.get("title") or "").strip()
            desc = (c.get("description") or "").strip()
            level = (c.get("level") or "").strip()
            tags = c.get("tags") or []
            tags_txt = " ".join([t for t in tags if isinstance(t, str)])
            course_id_to_text[cid] = f"{title}\n{desc}\nlevel: {level}\ntags: {tags_txt}".strip()

        # Build user profile from recent interactions (if user id is valid)
        user_profile = None
        if user_oid is not None:
            interactions = list(
                self.db["interactions"]
                .find({"user": user_oid}, {"course": 1, "action": 1, "createdAt": 1})
                .sort("createdAt", -1)
                .limit(self.user_history_limit)
            )
            history_course_oids = [i["course"] for i in interactions if isinstance(i.get("course"), ObjectId)]
            if history_course_oids:
                history_courses = list(
                    self.db["courses"].find(
                        {"_id": {"$in": history_course_oids}},
                        {"title": 1, "description": 1, "tags": 1, "level": 1},
                    )
                )
                history_texts = [course_id_to_text.get(str(c["_id"])) for c in history_courses]
                history_texts = [t for t in history_texts if t]

                if history_texts:
                    hist_emb = self._embed(history_texts)
                    # simple mean
                    user_profile = hist_emb.mean(axis=0)

        # Embed candidates
        candidate_ids = list(course_id_to_text.keys())
        candidate_texts = [course_id_to_text[cid] for cid in candidate_ids]
        cand_emb = self._embed(candidate_texts)

        if user_profile is None:
            # Cold-start: return candidates as-is (preserve input order, truncated)
            # (backend fallback handles popularity; here we just avoid 500)
            return candidate_ids[:top_k]

        # Cosine similarity
        user_vec = user_profile / (np.linalg.norm(user_profile) + 1e-12)
        cand_norm = cand_emb / (np.linalg.norm(cand_emb, axis=1, keepdims=True) + 1e-12)
        scores = cand_norm @ user_vec

        ranked_idx = np.argsort(-scores)[:top_k]
        ranked_ids = [candidate_ids[int(i)] for i in ranked_idx]
        return ranked_ids

    def _embed(self, texts: Iterable[str]) -> np.ndarray:
        emb = self._model.encode(list(texts), normalize_embeddings=False)
        return np.asarray(emb, dtype=np.float32)