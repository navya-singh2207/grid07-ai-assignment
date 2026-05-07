import math
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine, get_db
from .models import College, RankCutoff
from .schemas import (
    CollegeDetail,
    CompareRequest,
    CompareResponse,
    CompareRow,
    PaginatedCollegeResponse,
    PredictorRequest,
    PredictorResponse,
    PredictorResult,
)
from .seed_data import seed

app = FastAPI(title="College Discovery API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/colleges", response_model=PaginatedCollegeResponse)
def list_colleges(
    search: Optional[str] = Query(default=None),
    location: Optional[str] = Query(default=None),
    course: Optional[str] = Query(default=None),
    max_fees: Optional[int] = Query(default=None, ge=1),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=6, ge=1, le=50),
    db: Session = Depends(get_db),
):
    filters = []
    if search:
        filters.append(College.name.ilike(f"%{search.strip()}%"))
    if location:
        filters.append(College.location == location)
    if course:
        filters.append(College.courses_csv.ilike(f"%{course.strip()}%"))
    if max_fees is not None:
        filters.append(College.fees <= max_fees)

    query = db.query(College)
    if filters:
        query = query.filter(and_(*filters))

    total = query.count()
    total_pages = max(math.ceil(total / page_size), 1)
    offset = (page - 1) * page_size
    items = (
        query.order_by(College.rating.desc(), College.name.asc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }


@app.get("/api/colleges/{college_id}", response_model=CollegeDetail)
def get_college(college_id: int, db: Session = Depends(get_db)):
    college = db.query(College).filter(College.id == college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")

    return {
        "id": college.id,
        "name": college.name,
        "location": college.location,
        "fees": college.fees,
        "rating": college.rating,
        "placement_percent": college.placement_percent,
        "courses": [c.strip() for c in college.courses_csv.split(",") if c.strip()],
        "overview": college.overview,
        "placements_info": college.placements_info,
        "reviews_info": college.reviews_info,
    }


@app.post("/api/compare", response_model=CompareResponse)
def compare_colleges(payload: CompareRequest, db: Session = Depends(get_db)):
    colleges = db.query(College).filter(College.id.in_(payload.college_ids)).all()
    if len(colleges) < 2:
        raise HTTPException(status_code=400, detail="Select at least 2 valid colleges")

    items: List[CompareRow] = [
        CompareRow(
            id=c.id,
            name=c.name,
            fees=c.fees,
            placement_percent=c.placement_percent,
            rating=c.rating,
            location=c.location,
        )
        for c in colleges
    ]
    return {"items": items}


@app.post("/api/predictor", response_model=PredictorResponse)
def predictor(payload: PredictorRequest, db: Session = Depends(get_db)):
    normalized_exam = payload.exam.strip().upper()
    cutoffs = (
        db.query(RankCutoff, College)
        .join(College, College.id == RankCutoff.college_id)
        .filter(
            and_(
                func.upper(RankCutoff.exam) == normalized_exam,
                RankCutoff.max_rank >= payload.rank,
            )
        )
        .order_by(RankCutoff.max_rank.asc())
        .limit(6)
        .all()
    )

    results = [
        PredictorResult(
            college_id=college.id,
            college_name=college.name,
            location=college.location,
            estimated_cutoff=cutoff.max_rank,
        )
        for cutoff, college in cutoffs
    ]

    return {
        "exam": normalized_exam,
        "rank": payload.rank,
        "suggestions": results,
    }
