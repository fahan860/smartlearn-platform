from pydantic import BaseModel, Field
from typing import List


class RecommendRequest(BaseModel):
	userId: str = Field(..., min_length=1)
	candidateCourseIds: List[str] = Field(default_factory=list)
	excludeCourseIds: List[str] = Field(default_factory=list)
	topK: int = Field(default=20, ge=1, le=100)


class RecommendResponse(BaseModel):
	courseIds: List[str]
