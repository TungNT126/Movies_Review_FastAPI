from sqlmodel import  Field, Column, SQLModel
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

    title: str = Field(max_length=200, index=True)
    director: str = Field(index=True)
    duration: int = Field(index=True, gt=0)
    released_year: int = Field(gt=1900)

    def __repr__(self):
        return f"<Movie {self.title}>"