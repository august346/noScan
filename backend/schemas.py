import datetime
from typing import Optional

from pydantic import BaseModel


class BrandLikesBase(BaseModel):
    created: datetime.datetime
    likes: Optional[int] = None


class BrandLikes(BrandLikesBase):
    id: int
    brand_id: int

    class Config:
        orm_mode = True


class BrandBase(BaseModel):
    external_id: int
    url: str
    name: str
    logo_path: str
    empty: Optional[bool] = None


class Brand(BrandBase):
    id: int
    letter_id: int
    # likes: list[BrandLikes] = []

    class Config:
        orm_mode = True


class LetterBase(BaseModel):
    name: str
    link: str


class Letter(LetterBase):
    id: int
    brands: list[Brand] = []

    class Config:
        orm_mode = True
