from sqlalchemy import Column, Float, Integer, String, Text

from .database import Base


class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    location = Column(String(120), nullable=False, index=True)
    fees = Column(Integer, nullable=False, index=True)
    rating = Column(Float, nullable=False)
    placement_percent = Column(Float, nullable=False)
    courses_csv = Column(Text, nullable=False)
    overview = Column(Text, nullable=False)
    placements_info = Column(Text, nullable=False)
    reviews_info = Column(Text, nullable=False)


class RankCutoff(Base):
    __tablename__ = "rank_cutoffs"

    id = Column(Integer, primary_key=True, index=True)
    exam = Column(String(50), nullable=False, index=True)
    college_id = Column(Integer, nullable=False, index=True)
    max_rank = Column(Integer, nullable=False, index=True)
