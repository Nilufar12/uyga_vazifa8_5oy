from typing import Optional

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True


class NewsCreate(BaseModel):
    title: str
    views: int
    description: str
    image: Optional[str] = None
    video: Optional[str] = None

    category_id: int


class NewsResponse(NewsCreate):
    id: int

    class Config:
        from_attributes = True

