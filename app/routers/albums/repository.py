from typing import List

import beets
import beets.ui
from plugin.beets.beetsplug.wlg import WhatLastGenre

from girandole.app.types import Album


beets_lib = beets.ui._open_library(beets.config)


def get_all_albums() -> List[Album]:
    albums = map(Album.parse_obj, beets_lib.albums())
    return albums


def get_album_by_id(album_id: int) -> Album:
    album = Album.parse_obj(beets_lib.get_album(album_id))
    return album


def get_album_genre_suggestions(album_id: int) -> List[str]:
    album = beets_lib.get_album(album_id)

    wlg = WhatLastGenre()
    wlg.setup()
    genres = wlg.genres(album, dry=True).split(', ')

    return genres