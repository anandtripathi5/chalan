import importlib
import os
from datetime import datetime

from mako.template import Template

from constants import VERSIONS_DIR
from utils.exceptions import Exc


class Migrate:
    def __init__(self, es, config):
        self.es = es
        self.config = config

    def _index_exists(self):
        if not self.es.client:
            self.es.init()
            self.es.create_version_index()

    def _check_if_version_exists(self, version):
        for file_name in os.listdir(self.config.versions):
            file = f'{self.config.mig_dir}.{VERSIONS_DIR}.' + \
                   file_name.split('.')[0]
            file_module = importlib.import_module(file)
            if hasattr(file_module,
                       'down_revision') and file_module.down_revision == version:
                raise Exc(
                    "Revision [red bold]outdated[/red bold]. Upgrade to the latest revision and then create a new one.")

    def create_revision(self, message):
        self._index_exists()
        version = self.es.current_version()
        self._check_if_version_exists(version)
        revision = 1 if version is None else int(version) + 1
        content = Template(filename='templates/script.py.mako').render(
            message=message,
            create_date=datetime.now(),
            down_revision=version,
            revision=revision
        )
        with open(
                self.config.versions + f'/{revision}_{"_".join(message.split(" "))}.py',
                'w') as f:
            f.write(content)
