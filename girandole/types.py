from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Optional, List, Any

import beets.library
from pydantic import BaseModel, DirectoryPath, ConstrainedStr, errors


def padded_int(size, digit=0):
    class PaddedInt(str):
        @classmethod
        def __get_validators__(cls):
            yield cls.add_padding

        @classmethod
        def add_padding(cls, v):
            return f'{v:>{size}}'.replace(' ', str(digit))

    return PaddedInt


def csv(element_char, sep=',', field_type=str):
    class Csv(ConstrainedStr):
        @classmethod
        def __get_validators__(cls):
            yield cls.validate
            yield cls.parse_values

        @classmethod
        def validate(cls ,v):
            regex = f'^{element_char}+$|^(({element_char}+{sep})+{element_char})'
            r = re.compile(regex)
            if r.match(v):
                return v
            else:
                raise errors.StrRegexError(pattern=r.pattern)

        @classmethod
        def parse_values(cls, v):
            return list(map(field_type, v.split(sep)))

    return Csv


AlbumId = int
AlbumIds = csv(element_char=r'[\d]', sep=',', field_type=int)
Queries = csv(element_char=r'[^\/]', sep='/', field_type=str)


class Item(BaseModel):
    pass


class Album(BaseModel):
    @classmethod
    def from_beets_lib(cls, album: beets.library.Album) -> Album:
        try:
            artpath = album.artpath.decode('utf8')
        except (TypeError, AttributeError):
            artpath = None

        # TODO: Tidy this up.
        # - Use some sort of `PathType` or something. Also look at the
        #   Beets library API as well; how did they handle paths?
        # - Also, the dictcomp and non-explicitness feel dirty.
        return cls(**{field: getattr(album, field) for field in album.keys() if field != 'artpath'},
                   artpath=artpath,
                   path=album.item_dir().decode('utf8'))

    id: AlbumId
    added: datetime.datetime
    artpath: Optional[Path]
    albumartist: str
    albumartist_sort: str
    albumartist_credit: str
    album: str
    genre: str
    style: Optional[str]
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
    path: Path
    # items: Optional[List[Item]]


class GenresSuggestion(BaseModel):
    album_id: AlbumId
    suggested_genres: Optional[List[str]]


class BaseResponse(BaseModel):
    results: Any


class AlbumsResponse(BaseResponse):
    results: List[Album]


class GenresSuggestionResponse(BaseResponse):
    results: List[GenresSuggestion]
