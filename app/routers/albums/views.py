from typing import List

from fastapi import APIRouter, Path

import girandole.app.routers.albums.repository as repository
from girandole.app.types import AlbumsResponse, GenresSuggestionResponse, AlbumId, Queries, AlbumIds


router = APIRouter()


@router.get('/', response_model=AlbumsResponse)
async def get_all_albums():
    albums = repository.get_all_albums()
    return {'albums': albums}


@router.get('/query/{queries:path}', response_model=AlbumsResponse)
async def get_albums_by_queries(queries: Queries = Path(...)):
    return {'albums': []}


@router.get('/{album_ids}', response_model=AlbumsResponse)
async def get_albums_by_ids(album_ids: AlbumIds = Path(...)):
    albums = repository.get_albums_by_ids(album_ids)
    return {'albums': albums}

    
@router.get('/{album_ids}/genres', response_model=GenresSuggestionResponse)
async def get_albums_genre_suggestions(album_id: AlbumIds = Path(...)):
    genres_suggestion = repository.get_album_genre_suggestions(album_id)
    return {
        'albums': genres_suggestion,
    }




"""

@app.route('/album/query/')
@app.route('/album/query/<query:queries>')
@app.route('/album/<int:album_id>/art')
@app.route('/album/values/<string:key>')



"""