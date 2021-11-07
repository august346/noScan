import datetime
from typing import Optional

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from db import db

db.Base.metadata.create_all()
app = FastAPI()


def get_session():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_dt(diff: datetime.timedelta = datetime.timedelta()):
    return datetime.datetime.utcnow() - diff


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/brands/", response_model=list[schemas.Brand])
def read_brands(
    is_empty: bool = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    brands = crud.get_brands(session, skip=skip, limit=limit, is_empty=is_empty)
    return brands


@app.get("/likes/", response_model=list[schemas.BrandLikes])
def read_likes(
    brand_id: Optional[int] = None,
    start: Optional[datetime.datetime] = None,
    end: Optional[datetime.datetime] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    brands = crud.get_likes(session, skip=skip, limit=limit, brand_id=brand_id, start=start, end=end)
    return brands
