from typing import List, Iterable

import beets
import beets.ui
from plugin.beets.beetsplug.wlg import WhatLastGenre

from girandole.app.types import Album, AlbumId, GenresSuggestion


beets_lib = beets.ui._open_library(beets.config)


def get_all_albums() -> List[Album]:
    albums = list(map(Album.parse_obj, beets_lib.albums()))
    return albums


def get_album_by_id(album_id: AlbumId) -> Album:
    album = Album.parse_obj(beets_lib.get_album(album_id))
    return album


def get_albums_by_ids(album_ids: Iterable[AlbumId]) -> List[Album]:
    albums = [get_album_by_id(album_id) for album_id in album_ids]
    return albums


def get_album_genre_suggestions(album_id: AlbumId) -> List[GenresSuggestion]:
    album = beets_lib.get_album(album_id)

    wlg = WhatLastGenre()
    wlg.setup()
    genres_suggestion = wlg.genres(album, dry=True).split(', ')

    return [{
        'album_id': album_id,
        'suggestions': genres_suggestion
    }]