# Copyright 2017 TsumiNa. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# change version in there, conf.yml, setup.py
__all__ = ['descriptor', 'model', 'utils', 'visualization']


def _get_package_info(key):
    import yaml
    from pathlib import Path
    cwd = Path(__file__).parent / 'conf.yml'
    with open(str(cwd), 'r') as f:
        info = yaml.load(f)
    return info[key]


def _init(force=False):
    """
    Create config file is not exist at ~/.xenonpy/conf.yml

    .. warning::

        Set ``force=True`` will reset all which under the ``~/.xenonpy`` dir.

    Args
    ----
    force: bool
        force reset ``conf.yml`` to default and empty all dirs under ``~/.xenonpy``.
    """
    from shutil import rmtree, copyfile
    from ruamel.yaml import YAML
    from sys import version_info
    from pathlib import Path
    from ._conf import get_conf

    if version_info[0] != 3 or version_info[1] < 5:
        raise SystemError("Must be using Python 3.5 or 3.6")

    yaml = YAML(typ='safe')
    yaml.indent(mapping=2, sequence=4, offset=2)
    root_dir = Path.home() / __cfg_root__
    root_dir.mkdir(parents=True, exist_ok=True)
    user_cfg_file = root_dir / 'conf.yml'

    if force:
        rmtree(str(root_dir))

    # copy default conf.yml to ~/.xenonpy
    if not user_cfg_file.exists() or force:
        copyfile(str(Path(__file__).parent / 'conf.yml'), str(user_cfg_file))
    else:
        with open(str(user_cfg_file), 'r') as f:
            user_cfg = yaml.load(f)
        if 'version' not in user_cfg or user_cfg['version'] != __version__:
            with open(str(Path(__file__).parent / 'conf.yml'), 'r') as f:
                pack_cfg = yaml.load(f)
            pack_cfg['userdata'] = user_cfg['userdata']
            pack_cfg['usermodel'] = user_cfg['usermodel']
            pack_cfg['model_extern_backend'] = user_cfg['model_extern_backend']
            with open(str(user_cfg_file), 'w') as f:
                yaml.dump(pack_cfg, f)

    # init dirs
    dataset_dir = root_dir / 'dataset'
    cached_dir = root_dir / 'cached'
    user_data_dir = Path(get_conf('userdata')).expanduser()
    user_model_dir = Path(get_conf('usermodel')).expanduser()

    # create dirs
    dataset_dir.mkdir(parents=True, exist_ok=True)
    cached_dir.mkdir(parents=True, exist_ok=True)
    user_data_dir.mkdir(parents=True, exist_ok=True)
    user_model_dir.mkdir(parents=True, exist_ok=True)


__version__ = _get_package_info('version')
__release__ = _get_package_info('release')
__short_description__ = _get_package_info('short_description')
__license__ = _get_package_info('license')
__author__ = _get_package_info('author')
__author_email__ = _get_package_info('author_email')
__maintainer__ = _get_package_info('maintainer')
__maintainer_email__ = _get_package_info('maintainer_email')
__github_username__ = _get_package_info('github_username')
__cfg_root__ = '.' + __name__

from . import descriptor
from . import model
# from .pipeline import *
# from .preprocess import *
from . import utils
from . import visualization

_init()
