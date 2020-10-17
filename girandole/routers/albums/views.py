import logging
import os
from pathlib import PureWindowsPath, PurePath
from typing import List

import beets.library
from fastapi import APIRouter, Path, Request, Body, HTTPException
from starlette.responses import FileResponse

import girandole.routers.albums.repository as repository
import girandole.utils
from girandole.api_models import AlbumsResponse, GenresSuggestionResponse, AlbumId, Queries, AlbumIds
from girandole.config import Config


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('/', response_model=AlbumsResponse)
async def get_all_albums():
    albums = repository.get_all_albums()
    return {'results': albums}


@router.get('/query/{queries:path}', response_model=AlbumsResponse)
async def get_albums_by_query(queries: Queries = Path(...)):
    # TODO: Implement.
    albums = repository.get_albums_by_query(queries)
    return {'results': albums}


@router.get('/{album_ids}', response_model=AlbumsResponse)
async def get_albums_by_ids(album_ids: AlbumIds = Path(...)):
    albums = repository.get_albums_by_ids(album_ids)
    return {'results': albums}

    
@router.get('/{album_ids}/genres', response_model=GenresSuggestionResponse)
async def get_albums_genre_suggestions(album_ids: AlbumIds = Path(...)):
    genres_suggestion = repository.get_albums_genres_suggestions(album_ids)
    return {'results': genres_suggestion}


@router.get('/{album_id}/art')
async def get_album_art(album_id: AlbumId):
    album = repository.get_album_by_id(album_id)

    try:
        new_base_path = PurePath(os.environ('GIRANDOLE_MUSIC_DIR'))
    except TypeError:
        new_base_path = None

    if new_base_path:
        uses_windows_paths = Config['beets'].getboolean('windows paths', False)
        if uses_windows_paths:
            album_art_path = girandole.utils.path_from_beets(album.artpath, PureWindowsPath)
            base_path_in_db = PureWindowsPath(beets.config['directory'].get())
        else:
            album_art_path = girandole.utils.path_from_beets(album.artpath)
            base_path_in_db = PurePath(beets.config['directory'].get())

        # Rebase if necessary.
        if new_base_path not in album_art_path.parents:
            album_art_path = girandole.utils.rebase_path(
                album_art_path, base_path_in_db, new_base_path)
    else:
        album_art_path = girandole.utils.path_from_beets(album.artpath)

    if not album_art_path:
        raise HTTPException(
            status_code=404,
            detail=f"Album '{album.albumartist} - {album.album} "
                   f"({album.year})' with ID '{album_id}' has no album art.")
    return FileResponse(album_art_path, media_type='image/jpeg')


@router.post('/{album_ids}/genres', response_model=AlbumsResponse)
async def post_album_genres(album_ids: AlbumIds, genres: List[str], write_tags: bool = False):
    try:
        # For now, use the setting from '.env'. In the future this will be
        # decided by Red Candle and passed in via the `write_tags` param.
        albums = repository.update_album_genres(album_ids, genres, write_tags=write_tags)
    except beets.library.ReadError:
        raise HTTPException(
            status_code=500,
            detail=f"Could not read file. Make sure "
                   f"it exists and that you have the necessary "
                   f"permissions.")
    except beets.library.WriteError:
        raise HTTPException(
            status_code=500,
            detail=f"Could not write to file. Make sure "
                   f"it exists and that you have the necessary "
                   f"permissions.")
    return {'results': albums}
