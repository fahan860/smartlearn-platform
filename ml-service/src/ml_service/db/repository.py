import logging


logger = logging.getLogger(__name__)


class RecommendationRepository:
    def save_recommendation_event(self, user_id: str, selected_course_ids: list[str]) -> None:
        logger.debug(
            "Recommendation event not persisted (repository adapter not configured). user_id=%s count=%s",
            user_id,
            len(selected_course_ids),
        )