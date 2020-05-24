from io import BytesIO
from pathlib import Path
from typing import List, Iterable, Tuple

import beets
import beets.library
import beets.ui
from plugin.beets.beetsplug.wlg import WhatLastGenre

from girandole.types import Album, AlbumId, GenresSuggestion, Queries


beets_lib = beets.ui._open_library(beets.config)


def get_all_albums() -> List[Album]:
    albums = list(map(Album.parse_obj, beets_lib.albums()))
    return albums


def get_album_by_id(album_id: AlbumId) -> Album:
    album = Album.parse_obj(beets_lib.get_album(album_id))
    return album


def get_albums_by_ids(album_ids: Iterable[AlbumId]) -> List[Album]:
    albums = list(map(get_album_by_id, album_ids))
    return albums


def get_album_genres_suggestion(album_id: AlbumId) -> GenresSuggestion:
    album = beets_lib.get_album(album_id)

    wlg = WhatLastGenre()
    wlg.setup()
    genres_suggestion = wlg.genres(album, dry=True).split(', ')

    return GenresSuggestion(album_id=album_id, suggested_genres=genres_suggestion)


def get_albums_genres_suggestions(album_ids: List[AlbumId]) -> List[GenresSuggestion]:
    genres_suggestions = list(map(get_album_genres_suggestion, album_ids))
    return genres_suggestions


def get_albums_by_query(query: Queries) -> List[Album]:
    return get_all_albums()


def get_db_album_by_id(album_id: AlbumId) -> beets.library.Album:
    album = beets_lib.get_album(album_id)
    return album


def update_album_genres(album_ids: List[AlbumId], genres: List[str], write_tags: bool = False) -> List[Album]:
    result = []
    for album_id in album_ids:
        db_album = beets_lib.get_album(album_id)
        db_album.genre = genres[0]
        db_album.store()
        if write_tags:
            for item in db_album.items():
                item.try_write()
        result.append(db_album)

    return result
