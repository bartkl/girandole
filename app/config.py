from pathlib import Path

from girandole.app.utils import config as config_utils


CONFIG = config_utils.read_yaml(Path('/app') / 'config' / 'app_config.yaml')