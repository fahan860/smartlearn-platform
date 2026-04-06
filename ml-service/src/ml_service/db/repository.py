import logging
from datetime import datetime, timezone

from bson import ObjectId

from ml_service.db.mongo_client import get_db

logger = logging.getLogger(__name__)


class RecommendationRepository:
    def __init__(self) -> None:
        self._db = get_db()

    def save_recommendation_event(self, user_id: str, selected_course_ids: list[str]) -> None:
        user_oid = ObjectId(user_id) if ObjectId.is_valid(user_id) else user_id
        course_oids = [
            ObjectId(cid) if ObjectId.is_valid(cid) else cid
            for cid in (selected_course_ids or [])
        ]

        doc = {
            "user": user_oid,
            "selectedCourseIds": course_oids,
            "createdAt": datetime.now(timezone.utc),
        }

        self._db["recommendation_events"].insert_one(doc)
        logger.info("Recommendation event persisted. user_id=%s count=%s", user_id, len(course_oids))