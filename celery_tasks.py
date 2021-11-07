import logging
from typing import Iterable

from celery.signals import worker_ready
from sqlalchemy.orm import Session

import db
from celery_app import app
from collect.collector import get_letters, get_brands, is_empty, get_likes
from collect.extractor import Letter, Brand


logging.basicConfig(level=logging.INFO)     # for local debug


@worker_ready.connect
def at_start(*args, **kwargs):
    collect_full()


@app.task
def collect_full():
    with Session(db.engine) as session:
        for let, let_obj in collect_letters(session):
            for br, br_obj in collect_brands(session, let, let_obj):
                logging.info(br_obj)


@app.task
def update_empties():
    with Session(db.engine) as session:
        brands: Iterable[db.Brand] = session.query(db.Brand).filter(db.Brand.empty)
        already_not_empty: Iterable[db.Brand] = filter(
            lambda obj: not is_empty(Brand.from_obj(obj)),
            brands
        )

        ind: int = 0
        for ind, br_obj in enumerate(already_not_empty, start=1):
            br_obj.empty = False
            session.commit()

            logging.info(f"updated already not empty: {br_obj}")

        logging.info(f"total updated not empty: {ind}")


@app.task()
def collect_letters(session: Session) -> Iterable[tuple[Letter, db.Letter]]:
    letter_list = get_letters()
    for letter in letter_list:
        yield letter, db.get_or_create(
            session=session,
            model=db.Letter,
            dataclass=letter
        )


@app.task
def collect_brands(session: Session, letter: Letter, letter_obj: db.Letter) -> Iterable[tuple[Brand, db.Brand]]:
    brand_list = get_brands(letter)
    for brand in brand_list:
        yield brand, db.get_or_create(
            session=session,
            model=db.Brand,
            dataclass=brand,
            letter_id=letter_obj.id,
            empty=is_empty(brand)
        )


@app.task
def collect_likes():
    with Session(db.engine) as session:
        ind = 0
        for ind, br_obj in enumerate(session.query(db.Brand).filter(db.Brand.empty), start=1):
            likes_obj: db.BrandLikes = db.BrandLikes(likes=get_likes(br_obj))
            br_obj.likes.append(likes_obj)
            session.commit()

            logging.info(f'likes collected: {likes_obj}')

        logging.info(f'total likes collected: {ind}')
