from pydantic import BaseModel
from typing import List

# Article inside UserDisplay
class Article(BaseModel):
    title: str
    content: str
    published: bool
    class Config():
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str
    password: str

# Configure the output json on api endpoint to display only username and email
class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Article] = []
    class Config():
        from_attributes = True

# User inside ArticleDisplay
class User(BaseModel):
    id: int
    username: str
    class Config():
        from_attributes = True

class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int

class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User
    class Config():
        from_attributes = True

class ProductBase(BaseModel):
    title: str
    description: str
    price: float