from typing import List

from fastapi import APIRouter

import girandole.app.routers.albums.repository as repository
from girandole.app.types import Album, GenresSuggestion


router = APIRouter()


@router.get('/', response_model=List[Album])
def get_all_albums():
    albums = list(repository.get_all_albums())
    return albums


@router.get('/{album_id}', response_model=Album)
def get_album_by_id(album_id: int):
    album = repository.get_album_by_id(album_id)
    return album


@router.get('/{album_id}/genres', response_model=GenresSuggestion)
def get_album_genre_suggestions(album_id: int):
    genres = repository.get_album_genre_suggestions(album_id)
    return {
        'album_id': album_id,
        'suggestions': genres
    }
