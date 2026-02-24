from ml_service.models.schemas import RecommendRequest


def build_candidate_pool(payload: RecommendRequest) -> list[str]:
    excluded = set(payload.excludeCourseIds)
    return [course_id for course_id in payload.candidateCourseIds if course_id not in excluded]