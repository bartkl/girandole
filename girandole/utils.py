import os
import beets.util


def is_posix_path(path):
    return path[0] == '/'


def rebase_path(path, basepath, new_basepath):
    path, basepath, new_basepath = \
        map(beets.util.displayable_path,
        	(path, basepath, new_basepath))

    if not path.startswith(basepath):
        raise ValueError("Provided base path doesn't occur in path.")

    if is_posix_path(basepath):
        from posixpath import sep
    else:
        from ntpath import sep

    relpath = path.split(basepath + sep)[1]

    if is_posix_path(new_basepath):
        from ntpath import sep as from_sep
        from posixpath import sep as to_sep
    else:
        from posixpath import sep as from_sep
        from ntpath import sep as to_sep

    new_path = os.path.join(new_basepath, relpath.replace(from_sep, to_sep))

    return beets.util.normpath(new_path)
