import importlib
import os
from datetime import datetime
from pydoc import importfile
from rich import print
from mako.template import Template

from .constants import VERSIONS_DIR
from .utils.exceptions import Exc


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
        content = Template(filename=os.path.dirname(
            os.path.abspath(__file__)) + '/templates/script.py.mako').render(
            message=message,
            create_date=datetime.now(),
            down_revision=version,
            revision=revision
        )
        file_name = self.config.versions + f'/{revision}_{"_".join(message.split(" "))}.py'
        with open(file_name, 'w') as f:
            f.write(content)
            print(
                f"Migration file [green bold]{file_name}[/green bold] created successfully")

    def upgrade(self, version):
        self._index_exists()
        current_version = self.es.current_version()
        for file_name in os.listdir(self.config.versions):
            if '.py' not in file_name:
                continue
            file = importfile(self.config.versions + '/' + file_name)
            if hasattr(file,
                       'down_revision') and file.down_revision == current_version:
                file.upgrade(self.es.client)
                self.es.client.index(id='1',
                                     index=self.config.es['migration_index'],
                                     document=dict(version=file.revision),
                                     refresh=True)
                print(
                    f"********* {file.down_revision or 'HEAD'} ---> {file_name} *********")
                if version and version == file.revision:
                    break
                self.upgrade(version)
                break

    def downgrade(self, version, level=1):
        if version is None and level == 0:
            return
        self._index_exists()
        current_version = self.es.current_version()

        for file_name in os.listdir(self.config.versions):
            if '.py' not in file_name:
                continue
            file = importfile(self.config.versions + '/' + file_name)
            if hasattr(file,
                       'revision') and file.revision == current_version:
                file.downgrade(self.es.client)
                self.es.client.index(id='1',
                                     index=self.config.es['migration_index'],
                                     document=dict(version=file.down_revision),
                                     refresh=True)
                print(
                    f"********* {file_name}  ---> {file.down_revision or 'HEAD'} *********")
                if version and version == file.revision:
                    break
                if level > 0:
                    level -= 1
                self.downgrade(version, level)
