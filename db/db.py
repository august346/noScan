from datetime import datetime

import sqlalchemy as db
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import declarative_base, relationship, Session

engine = db.create_engine('mariadb+pymysql://root:root@localhost/brands?charset=utf8mb4')

meta = db.MetaData(bind=engine)
Base = declarative_base(metadata=meta)


class Letter(Base):
    __tablename__ = 'letters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    link = db.Column(db.String(100), unique=True)

    brands = relationship("Brand")


class Brand(Base):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.Integer, unique=True)
    url = db.Column(db.String(100))
    name = db.Column(db.String(100))
    logo_path = db.Column(db.String(100))
    empty = db.Column(db.Boolean, nullable=True)
    letter_id = db.Column(db.Integer, db.ForeignKey('letters.id'))

    letter = relationship('Letter', back_populates='brands')
    likes = relationship("BrandLikes")

    def __repr__(self):
        return f'{self.__class__.__name__}(id="{self.id}", name="{self.name}", url="{self.url}")'


class BrandLikes(Base):
    __tablename__ = 'brands_likes'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, nullable=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))

    brand = relationship('Brand', back_populates='likes')

    def __repr__(self):
        return f'{self.__class__.__name__}(created="{self.created}", likes="{self.likes}", brand="{self.brand}")'


def get_or_create(session: Session, model: Base, dataclass, **kwargs) -> Base:
    values = dataclass.data | kwargs
    insert_stmt = insert(model).values(**values)
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(values)

    session.execute(on_duplicate_key_stmt)
    session.commit()

    return session.query(model).filter(dataclass.filter).first()
