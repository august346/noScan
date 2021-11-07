from sqlalchemy.orm import Session

import db
from celery_app import app
from collect.collector import get_letters, get_brands, is_empty


@app.task
def collect():
    with Session(db.engine) as session:
        letter_list = get_letters()
        for letter in letter_list:
            letter_obj: db.Letter = db.get_or_create(
                session=session,
                model=db.Letter,
                dataclass=letter
            )
            brand_list = get_brands(letter)
            for brand in brand_list:
                brand_obj: db.Brand = db.get_or_create(
                    session=session,
                    model=db.Brand,
                    dataclass=brand,
                    letter_id=letter_obj.id,
                    empty=is_empty(brand)
                )
                print(['-', '+'][brand_obj.empty], letter_obj.name, brand_obj.name)
