import logging
import os
from io import BytesIO
from typing import List, Iterable, Tuple, Optional

import beets
import beets.library
import beets.ui
from plugin.beets.beetsplug.wlg import WhatLastGenre

from girandole.types import Album, AlbumId, GenresSuggestion, Queries
import girandole.utils


logger = logging.getLogger(__name__)
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


def update_album_genres(album_ids: List[AlbumId],
                        genres: List[str],
                        base_path: Optional[str] =
                            (os.environ.get('GIRANDOLE_MUSIC_DIR', '')),
                        write_tags: Optional[bool] = False) -> List[Album]:
    result = []
    for album_id in album_ids:
        db_album = beets_lib.get_album(album_id)
        db_album.genre = genres[0]  # Currently only setting a single genre is allowed.
        db_album.store()

        if write_tags:
            for item in db_album.items():
                music_dir = beets.config['directory'].as_filename()
                if base_path and base_path != music_dir:
                    item_path = girandole.utils.rebase_path(item.path, music_dir, base_path)
                else:
                    item_path = item.path
                try:
                    item.write(item_path)
                except (beets.library.ReadError, beets.library.WriteError):
                   # TODO: Implement decent error handling here.
                   raise 
        result.append(db_album)

    return result