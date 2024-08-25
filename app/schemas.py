from pydantic import BaseModel, EmailStr
from pydantic.types import conint

class User(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserCreate(User):
    pass


class UserUpdate(User):
    pass


class UserReturn(BaseModel):
    id: int
    email: str
    username: str


class UserLogin(BaseModel):
    username: str
    password: str


class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostUpdate(Post):
    is_published: bool


class PostCreate(Post):
    pass


class PostReturn(Post):
    id: int
    upvotes: int
    downvotes: int
    owner_id: int
    owner: UserReturn


class Token(BaseModel):
    access_token: str
    token_type: str


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
