import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import girandole.app.routers.albums.views
# from girandole.app.config import CONFIG as config


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(girandole.app.routers.albums.views.router, prefix="/album")