from pathlib import Path

import beets
import beetsplug.web
from flask import Blueprint, abort, g, request, current_app
from plugin.beets.beetsplug.wlg import WhatLastGenre


girandole = Blueprint('girandole', __name__)


# TODO: This view should not be part of this project.
@girandole.route("/cover-art/<everything:p>/cover.jpg")
def get_cover_art(p):
    full_path = beets.config['directory'].get()
    item_json = beetsplug.web.item_at_path(full_path).json
    if item_json:
        album_id = item_json['album_id']
        return beetsplug.web.album_art(album_id)
    else:
        abort(404)


@girandole.route("/album/<int:album_id>/genres")
def get_album_genres(album_id):
    album = g.lib.get_album(album_id)

    if not 'suggest' in request.args:
        return album.genre

    wlg = WhatLastGenre()
    wlg.setup()
    genres = wlg.genres(album, dry=True)
    return genres