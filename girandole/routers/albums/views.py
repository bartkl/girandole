from typing import List

from fastapi import APIRouter, Path, Request, Body, HTTPException
from starlette.responses import FileResponse

import girandole.routers.albums.repository as repository
from girandole.types import AlbumsResponse, GenresSuggestionResponse, AlbumId, Queries, AlbumIds


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
    db_album = repository.get_db_album_by_id(album_id)
    try:
        album_art_path = db_album.artpath.decode('utf8')
    except AttributeError:
        raise HTTPException(
            status_code=404,
            detail=f"Album '{db_album.albumartist} - {db_album.album} "
                   f"({db_album.year})' with ID 'album_id' has no album art.")
    return FileResponse(album_art_path, media_type='image/jpeg')


@router.post('/{album_ids}/genres', response_model=AlbumsResponse)
async def post_album_genres(album_ids: AlbumIds, genres: List[str]):
    albums = repository.update_album_genres(album_ids, genres, write_tags=True)
    return {'results': albums}
