from pydantic import BaseModel
from typing import List, Optional

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    id: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str
    username: str
    Password: str   

class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    Password: str

class ShowUser(BaseModel):
    name: str
    username: str
    blogs: List[Blog] =[]
    class Config:
        orm_mode = True

class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    Creator: ShowUser

    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    Password: str

class TokenData(BaseModel):
    username: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str
