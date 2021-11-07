import datetime

from sqlalchemy.orm import Session

from db import db


def get_brands(session: Session, skip: int = 0, limit: int = 100, is_empty: bool = None):
    filters = {} if is_empty is None else {"empty": is_empty}
    return session.query(db.Brand).filter_by(**filters).offset(skip).limit(limit).all()


def get_likes(
    session: Session,
    brand_id: int,
    start: datetime.datetime,
    end: datetime.datetime,
    skip: int = 0,
    limit: int = 100
):
    filters = []
    if brand_id:
        filters.append(db.BrandLikes.brand_id == brand_id)
    if start:
        filters.append(db.BrandLikes.created >= start)
    if end:
        filters.append(db.BrandLikes.created < end)

    return session.query(db.BrandLikes).filter(*filters).offset(skip).limit(limit).all()
