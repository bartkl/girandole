import os
import beets.util


def rebase_path(path, basepath, new_basepath):
    path, basepath, new_basepath = \
        map(beets.util.displayable_path,
        	(path, basepath, new_basepath))

    relpath = os.path.relpath(path, basepath)
    new_path = os.path.join(new_basepath, relpath)

    return beets.util.normpath(new_path)