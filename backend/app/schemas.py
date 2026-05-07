from typing import List

from pydantic import BaseModel, Field


class CollegeCard(BaseModel):
    id: int
    name: str
    location: str
    fees: int
    rating: float

    class Config:
        from_attributes = True


class CollegeDetail(CollegeCard):
    placement_percent: float
    courses: List[str]
    overview: str
    placements_info: str
    reviews_info: str


class PaginatedCollegeResponse(BaseModel):
    items: List[CollegeCard]
    page: int
    page_size: int
    total: int
    total_pages: int


class CompareRequest(BaseModel):
    college_ids: List[int] = Field(..., min_length=2, max_length=3)


class CompareRow(BaseModel):
    id: int
    name: str
    fees: int
    placement_percent: float
    rating: float
    location: str


class CompareResponse(BaseModel):
    items: List[CompareRow]


class PredictorRequest(BaseModel):
    exam: str
    rank: int = Field(..., gt=0)


class PredictorResult(BaseModel):
    college_id: int
    college_name: str
    location: str
    estimated_cutoff: int


class PredictorResponse(BaseModel):
    exam: str
    rank: int
    suggestions: List[PredictorResult]
