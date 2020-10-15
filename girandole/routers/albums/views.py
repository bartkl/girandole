import os
from typing import List

import beets.library
from fastapi import APIRouter, Path, Request, Body, HTTPException
from starlette.responses import FileResponse

import girandole.routers.albums.repository as repository
from girandole.api_models import AlbumsResponse, GenresSuggestionResponse, AlbumId, Queries, AlbumIds


router = APIRouter()


@router.get('/', response_model=AlbumsResponse)
async def get_all_albums():
    albums = repository.get_all_albums()
    return {'results': albums}


@router.get('/query/{queries:path}', response_model=AlbumsResponse)
async def get_albums_by_query(queries: Queries = Path(...)):
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
    album_art_path = album.artpath
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
        write_tags = {
            'no': False,
            'yes': True 
        }[os.environ.get('GIRANDOLE_WRITE_TAGS', 'no')]
        albums = repository.update_album_genres(album_ids, genres, write_tags=write_tags)
    except beets.library.ReadError:
        raise HTTPException(
            status_code=500,
            detail=f"Could not read file '{item_path}'. Make sure "
                   f"it exists and that you have the necessary "
                   f"permissions.")
    except beets.library.WriteError:
        raise HTTPException(
            status_code=500,
            detail=f"Could not write to file '{item_path}'. Make sure "
                   f"it exists and that you have the necessary "
                   f"permissions.")
    return {'results': albums}
