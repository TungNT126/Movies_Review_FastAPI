from typing import Optional
import uuid
from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    director: str
    duration: int
    released_year: int

class MovieCreateModel(MovieBase):
    pass

class MovieUpdateModel(MovieBase):
    title: Optional[str] = None
    director: Optional[str] = None
    duration: Optional[int] = None
    released_year: Optional[int] = None

class MovieReadModel(MovieBase):
    uid: uuid.UUID

    class Config:
        orm_mode = True