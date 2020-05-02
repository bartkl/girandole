import datetime
from typing import Optional, List

from pydantic import BaseModel, DirectoryPath


def padded_int(size, digit=0):
    class PaddedInt(str):
        @classmethod
        def __get_validators__(cls):
            yield cls.add_padding

        @classmethod
        def add_padding(cls, v):
            return f'{v:>{size}}'.replace(' ', str(digit))

    return PaddedInt


class Item(BaseModel):
    pass



class Album(BaseModel):
    id: int
    added: datetime.datetime
    albumartist: str
    albumartist_sort: str
    albumartist_credit: str
    album: str
    genre: str
    style: Optional[str] = None
    discogs_albumid: Optional[int]
    discogs_artistid: Optional[int]
    discogs_labelid: Optional[int]
    year: padded_int(4)
    month: padded_int(2)
    day: padded_int(2)
    disctotal: padded_int(2)
    comp: bool
    mb_albumid: str
    mb_albumartistid: str
    albumtype: str
    label: str
    mb_releasegroupid: str
    asin: str
    catalognum: str
    script: str
    language: str
    country: str
    albumstatus: str
    albumdisambig: str
    releasegroupdisambig: str
    rg_album_gain: Optional[float]
    rg_album_peak: Optional[float]
    r128_album_gain: Optional[padded_int(6)]
    original_year: padded_int(4)
    original_month: padded_int(2)
    original_day: padded_int(2)
    # items: Optional[List[Item]]
    # path: DirectoryPath


class GenresSuggestion(BaseModel):
    album_id: int
    suggestions: Optional[List[str]]