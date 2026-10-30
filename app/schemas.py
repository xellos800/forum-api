from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Annotated, List
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    model_config = ConfigDict(from_attributes=True)


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserOut(User):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Post(PostBase):
    id: int
    created_at: datetime
    owner: User

    model_config = ConfigDict(from_attributes=True)


class PostOut(PostBase):
    pass

    model_config = ConfigDict(from_attributes=True)


class PostWrapper(BaseModel):
    post: Post
    comments: int = 0
    likes: int = 0

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    username: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]


class Comment(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(Comment):
    pass


class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    user: User

    model_config = ConfigDict(from_attributes=True)


class CommentWrapper(BaseModel):
    post: Post
    comments: List[CommentOut]

    model_config = ConfigDict(from_attributes=True)
