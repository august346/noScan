from dataclasses import dataclass, asdict
from typing import Any

from bs4 import BeautifulSoup
from requests import Response

import db


class Extractor:
    _response: Response

    result: Any

    def __init__(self, rsp: Response):
        self._response = rsp

    def do(self):
        raise NotImplemented


@dataclass
class Letter:
    name: str
    link: str

    @property
    def filter(self):
        return db.Letter.name == self.name

    @property
    def data(self) -> dict[str, Any]:
        return asdict(self)


class LettersExtractor(Extractor):
    result = list[Letter]

    def do(self):
        data: dict = self._response.json()
        self.result = list(map(lambda x: Letter(**x), data['value']['letters']))


@dataclass
class Brand:
    id: int
    url: str
    name: str
    logoPath: str

    @property
    def filter(self) -> bool:
        return db.Brand.external_id == self.id

    @property
    def data(self) -> dict[str, Any]:
        return {
            'external_id': self.id,
            'url': self.url,
            'name': self.name,
            'logo_path': self.logoPath,
        }


class BrandsExtractor(Extractor):
    result: list[Brand]

    def do(self):
        data: dict = self._response.json()
        self.result = list(map(lambda x: Brand(**x), data['value']['brandsList']))


class WithoutGoodsExtractor(Extractor):
    result: bool

    def do(self):
        soup: BeautifulSoup = BeautifulSoup(self._response.content, features='html.parser')
        self.result = soup.find('div', class_="product-card-list") is None


class LikeExtractor(Extractor):
    result: int

    def do(self):
        data: dict = self._response.json()
        self.result = data['value']['votesCount']
