import os
from configparser import ConfigParser
from pathlib import Path


CONFIG_DIR = Path(os.environ.get('GIRANDOLE_CONFIG_DIR', '/etc/girandole'))

Config = ConfigParser()
Config.read(CONFIG_DIR / 'config.ini')
