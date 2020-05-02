from pathlib import Path

from girandole.app.utils import config as config_utils


# TODO: Make the dir path configurable with an environment variable.
CONFIG = config_utils.read_yaml(Path('/') / 'etc' / 'girandole' / 'config.yaml')