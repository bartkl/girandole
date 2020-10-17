import logging
import os
from io import BytesIO
from pathlib import Path, PureWindowsPath, PurePath
from typing import List, Iterable, Tuple, Optional

import beets
import beets.library
import beets.ui
from fastapi import HTTPException
from plugin.beets.beetsplug.wlg import WhatLastGenre

import girandole.utils
from girandole.config import Config
from girandole.api_models import Album, AlbumId, GenresSuggestion, Queries


logger = logging.getLogger(__name__)
beets_lib = beets.ui._open_library(beets.config)

wlg = WhatLastGenre()
wlg.setup()


def get_all_albums() -> List[Album]:
    albums = list(map(Album.from_beets_lib, beets_lib.albums()))
    return albums


def get_album_by_id(album_id: AlbumId) -> Album:
    album = Album.from_beets_lib(beets_lib.get_album(album_id))
    return album


def get_albums_by_ids(album_ids: Iterable[AlbumId]) -> List[Album]:
    albums = list(map(get_album_by_id, album_ids))
    return albums


def get_album_genres_suggestion(album_id: AlbumId) -> GenresSuggestion:
    album = beets_lib.get_album(album_id)
    genres_suggestion = wlg.genres(album, dry=True).split(', ')

    return GenresSuggestion(album_id=album_id, suggested_genres=genres_suggestion)


def get_albums_genres_suggestions(album_ids: List[AlbumId]) -> List[GenresSuggestion]:
    genres_suggestions = list(map(get_album_genres_suggestion, album_ids))
    return genres_suggestions


def get_albums_by_query(query: Queries) -> List[Album]:
    # TODO.
    return get_all_albums()


def update_album_genres(album_ids: List[AlbumId],
                        genres: List[str],
                        base_path: Optional[Path] = None,
                        write_tags: Optional[bool] = False) -> List[Album]:
    result = []
    for album_id in album_ids:
        db_album = beets_lib.get_album(album_id)
        db_album.genre = genres[0]  # Currently only setting a single genre is allowed.

        db_album.store()

        if write_tags or beets.config['import']['write'].get(bool):
            try:
                new_base_path = PurePath(base_path or os.environ.get('GIRANDOLE_MUSIC_DIR'))
            except TypeError:
                new_base_path = None

            if new_base_path:
                uses_windows_paths = Config['beets'].getboolean('windows paths', False)

                if uses_windows_paths:
                    first_item_path = girandole.utils.path_from_beets(
                        db_album.items()
                            .get()
                            .path,
                        PureWindowsPath)
                    album_path = first_item_path.parent

                    base_path_in_db = PureWindowsPath(beets.config['directory'].get())

                else:
                    album_path = girandole.utils.path_from_beets(db_album.path, PurePath)
                    base_path_in_db = PurePath(beets.config['directory'].get())

                # Check if paths already use the desired base path.
                if new_base_path in album_path.parents:
                    new_base_path = None

            for item in db_album.items():
                if uses_windows_paths:
                    item_path = girandole.utils.path_from_beets(item.path, PureWindowsPath)
                else:
                    item_path = girandole.utils.path_from_beets(item.path, PurePath)

                if new_base_path:
                    item_path = girandole.utils.rebase_path(
                        item_path, base_path_in_db, new_base_path)
                item.write(str(item_path))

        result.append(Album.from_beets_lib(db_album))

    return result
