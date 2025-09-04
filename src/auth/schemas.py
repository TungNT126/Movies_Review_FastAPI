from pydantic import BaseModel
from typing import Optional
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

class UserUpdateModel(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    is_verified: Optional[bool] = None

class UserSignUp(BaseModel):
    email: str
    password: str
