import logging
from typing import Optional

from db import db
from collect.extractor import LettersExtractor, Letter, Brand, BrandsExtractor, WithoutGoodsExtractor, LikeExtractor
from collect.requester import LettersRequester, BrandsRequester, WithoutGoodsRequester, LikeRequester


def get_letters() -> list[Letter]:
    lr = LettersRequester()
    lr.do()
    le = LettersExtractor(lr.response)
    le.do()
    return le.result


def get_brands(letter: Letter) -> list[Brand]:
    br = BrandsRequester(letter.name)
    br.do()

    if not br.is_2xx:
        logging.error(f'Failed collect letter=`{letter.name}` brands')
        return []

    be = BrandsExtractor(br.response)
    be.do()
    return be.result


def is_empty(brand: Brand) -> Optional[bool]:
    wgr = WithoutGoodsRequester(brand.url)
    wgr.do()

    if not wgr.is_2xx:
        logging.error(f'Failed check brand=`{brand.name}` products')
        return None

    wge = WithoutGoodsExtractor(wgr.response)
    wge.do()
    return wge.result


def get_likes(brand_obj: db.Brand) -> Optional[int]:
    lr = LikeRequester(brand_obj.external_id)
    lr.do()

    if not lr.is_2xx:
        logging.error(f'Failed get brand=`{brand_obj.name}` likes')
        return None

    le = LikeExtractor(lr.response)
    le.do()
    return le.result
