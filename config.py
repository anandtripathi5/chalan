import os
import sys
from configparser import ConfigParser
from os import path

import typer

from constants import CONFIG_INI, MIGRATION_DIR
from utils.exceptions import Exc
from rich import print


class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.directory = None

    def create_ini(self):
        if path.exists(CONFIG_INI):
            Exc("Config file [red bold]%s[/red bold] already exists" % CONFIG_INI)

        self.config['CHALAN'] = dict(
            directory=MIGRATION_DIR,
            path_prefix='./',
            es_host='%(ES_HOST)s'
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
