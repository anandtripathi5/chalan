import os
from configparser import SafeConfigParser
from os import path

from constants import CONFIG_INI, MIGRATION_DIR
from utils.exceptions import Exc


class Config:
    def __init__(self):
        self.config = SafeConfigParser()
        self.directory = None
        self._es = None

    def create_ini(self):
        if path.exists(CONFIG_INI):
            Exc("Config file [red bold]%s[/red bold] already exists" % CONFIG_INI)

        self.config['CHALAN'] = dict(
            directory=MIGRATION_DIR,
            path_prefix='./'
        )
        self.config['ES'] = dict(
            es_host='%(ES_HOST)s',
            es_user='%(ES_USER)s',
            es_pass='%(ES_PASS)s',
            migration_index='chalan_versions'
        )
        self.config.write(open(CONFIG_INI, "w"))

    @property
    def mig_dir(self):
        if not self.directory:
            self.config.read(CONFIG_INI)
            self.directory = self.config['CHALAN']['directory']
        return self.directory

    @property
    def versions(self):
        return os.path.join(self.mig_dir, "versions")

    @property
    def es(self):
        if not self._es:
            self.config.read('ES')
            self._es = self.config['ES']
        return self._es
