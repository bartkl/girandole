import os
import beets.util
from pathlib import PurePath, PureWindowsPath, PurePosixPath, PurePath
from typing import Union


def get_path_type(path):
    return PurePosixPath if str(path)[0] == '/' else PureWindowsPath


def rebase_path(path: PurePath, basepath: PurePath, new_basepath: PurePath):
    relpath = path.relative_to(basepath)

    new_basepath_type = get_path_type(new_basepath)
    relpath = new_basepath_type(relpath)

    new_path = new_basepath / relpath
    return new_path


def path_from_beets(beets_path: Union[str, bytes]):
    if isinstance(beets_path, bytes):
        beets_path = beets_path.decode('utf8')

    return PurePath(beets_path)