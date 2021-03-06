import os
import beets.util
from pathlib import PurePath, PureWindowsPath, PurePosixPath, PurePath
from typing import Union, Any, Optional


def get_path_type(path):
    return PurePosixPath if str(path)[0] == '/' else PureWindowsPath


def rebase_path(path: PurePath, basepath: PurePath, new_basepath: PurePath):
    # Make sure the arguments are consistent among each other. For instance,
    # for Windows paths use `WindowsPurePath`s for `path` and `basepath`, or
    # the logic won't work well.

    if type(path) != type(basepath):
        raise ValueError('`path` and `basepath` must be of the same type, i.e. both Windows or both Posix paths.')
    
    relpath = path.relative_to(basepath)

    new_basepath_type = get_path_type(new_basepath)
    relpath = new_basepath_type(relpath)

    new_path = new_basepath / relpath
    return new_path


def path_from_beets(path: Union[bytes, str], as_type: Optional[Any] = PurePath) -> PurePath:
    if isinstance(path, bytes):
        path = path.decode('utf8')

    return as_type(path)
