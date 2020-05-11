import os.path
import re
from pathlib import Path
from typing import Dict

import yaml


def read_yaml(yaml_file: Path) -> Dict:
    """Reads YAML file, substitutes `${VAR}' with the environment
    variable VAR and returns a parsed dictionary.
    """

    path_matcher = re.compile(r'.*\${([^}^{]+)\}.*')

    def path_constructor(loader, node):
        return os.path.expandvars(node.value)

    class EnvVarLoader(yaml.SafeLoader):
        pass

    EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
    EnvVarLoader.add_constructor('!path', path_constructor)

    with open(yaml_file) as f:
        config = yaml.load(f, Loader=EnvVarLoader)
        
    return config
