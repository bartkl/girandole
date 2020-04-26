from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# import wlg_controller
from girandole.app.config import CONFIG as config


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/album')
def get_album():
    return 'Hi'


# @app.get('/album')
# def get_albums(genre=None):
#     if genre is None:
#         filter_ = None
#     else:
#         filter_ = ('genre', genre)
#     albums = mpd_controller.get_album_dirs(filter_, exact_match=True)

#     return albums


# @app.get('/album/{file_path:path}')
# def get_album(file_path):
#     album = mpd_controller.get_album(file_path)

#     return album


# @app.get('/album/{file_path:path}/suggested_genres')
# def get_album_suggested_genres(file_path):
#     album_path = Path(config['mpd']['music directory']) / file_path
#     genres = wlg_controller.get_suggested_genres(album_path)

#     return genres
