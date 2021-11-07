import time
from functools import wraps
from typing import Callable
from urllib.parse import urljoin

import requests
from requests import Response


PAUSE = 2
MAX_RETRY = 5
RETRY_PAUSE = 5


def paused(func: Callable):
    paused.ts = None

    @wraps(func)
    def wrapper(*args, **kwargs):
        need_wait: bool = bool(PAUSE and paused.ts)
        if need_wait:
            min_time_from: float = paused.ts + PAUSE
            sleep_time: float = min_time_from - time.time()
            sleep_time = round(sleep_time, 2)

            if sleep_time > 0:
                time.sleep(sleep_time)

        result = func(*args, **kwargs)
        paused.ts = time.time()

        return result

    return wrapper


class Requester:
    _method: str

    response: Response

    @property
    def _path(self) -> str:
        raise NotImplemented

    @property
    def _url(self) -> str:
        return urljoin('https://www.wildberries.ru', self._path)

    @paused
    def do(self):
        for _ in range(MAX_RETRY):
            self.response = requests.request(method=self._method, url=self._url)
            if self.is_2xx:
                return

            time.sleep(RETRY_PAUSE)

    @property
    def is_2xx(self) -> bool:
        return bool(self.response) and 200 <= self.response.status_code < 300


class LettersRequester(Requester):
    _method = 'get'

    @property
    def _path(self) -> str:
        return '/wildberries/brandlist/data?letter=a'


class BrandsRequester(Requester):
    _method = 'get'

    def __init__(self, letter: str):
        self._letter = letter

    @property
    def _path(self) -> str:
        return f'/wildberries/brandlist/data?letter={self._letter}'


class WithoutGoodsRequester(Requester):
    _method = 'get'

    def __init__(self, brand_path: str):
        self._brand_path = brand_path

    @property
    def _path(self) -> str:
        return self._brand_path


class LikeRequester(Requester):
    _method = 'post'

    def __init__(self, brand_id: int):
        self.brand_id = brand_id

    def _path(self) -> str:
        return f'/favorites/brand/getvotes?brandId={self.brand_id}'
