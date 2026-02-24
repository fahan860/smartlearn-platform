from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    userId: str = Field(..., min_length=1)
    candidateCourseIds: list[str] = Field(default_factory=list)
    excludeCourseIds: list[str] = Field(default_factory=list)
    topK: int = Field(default=20, ge=1, le=100)


class RecommendResponse(BaseModel):
    courseIds: list[str]