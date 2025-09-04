from datetime import date
from typing import List, Optional
from sqlmodel import  Field, Column, Relationship, SQLModel
import uuid
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__="users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True) # 'exclude' - Không hiện lên khi gọi API

    reviews: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy':"selectin"}) 

    def __repr__(self):
        return f"<User {self.username}>"



class Movie(SQLModel, table=True):
    __tablename__="movies"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )

    title: str = Field(max_length=200, index=True, unique=True)
    director: str = Field(index=True)
    duration: int = Field(index=True, gt=0)
    released_year: int = Field(gt=1900)

    reviews: List["Review"] = Relationship(back_populates="movie", sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self):
        return f"<Movie {self.title}>"
    
    
class Review(SQLModel, table=True):
    __tablename__="review"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )

    score: float = Field(ge=0, le=5, nullable=False)
    review: str = Field(max_length=250)
    review_date: date

    movie_uid: uuid.UUID = Field(default=None, foreign_key="movies.uid")
    movie: Optional["Movie"] = Relationship(back_populates="reviews")

    user_uid: uuid.UUID = Field(default=None, foreign_key="users.uid")
    user: Optional["User"] = Relationship(back_populates="reviews")   
  

    def __repr__(self):
        return f"<Review {self.uid} Score={self.score}>"    