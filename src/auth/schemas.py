from pydantic import BaseModel
from sqlmodel import Field


class UserBase(BaseModel):
    username: str = Field(max_length=8)
    email: str
    first_name: str
    last_name: str
    password_hash: str
    is_verified: bool


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: str
    first_name: str
    last_name: str
    password: str = Field(min_length=6)

class UserSignUp(BaseModel):
    email: str
    password: str
