from datetime import date
from pydantic import BaseModel
from typing import Optional
import uuid


class ReviewBase(BaseModel):
    score: int
    review: str
    review_date: date
    movie_uid: uuid.UUID

class ReviewCreateModel(ReviewBase):
    pass

class ReviewUpdateModel(ReviewBase):
    score: Optional[int]
    review: Optional[str]
    review_date: Optional[date]
    movie_uid: Optional[uuid.UUID]