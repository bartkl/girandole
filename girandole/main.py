import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import girandole.routers.albums.views
# from girandole.config import CONFIG as config


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(girandole.routers.albums.views.router, prefix="/album")
