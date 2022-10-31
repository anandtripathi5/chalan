import configparser
import os
from os import path

from mako.template import Template

from .constants import CONFIG_INI, VERSIONS_DIR
from .utils.exceptions import Exc


class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser(
            interpolation=EnvInterpolation())
        self.directory = None
        self._es = None

    def create_ini(self):
        if path.exists(CONFIG_INI):
            Exc("Config file [red bold]%s[/red bold] already exists" % CONFIG_INI)

        template = Template(filename=os.path.dirname(
            os.path.abspath(__file__)) + '/templates/chalan.ini.mako').render()
        with open(CONFIG_INI, 'w') as f:
            f.write(template)

    @property
    def mig_dir(self):
        if not self.directory:
            self.config.read(CONFIG_INI)
            self.directory = self.config['CHALAN']['directory']
        return self.directory

    @property
    def versions(self):
        return os.path.join(self.mig_dir, VERSIONS_DIR)

    @property
    def es(self):
        if not self._es:
            self.config.read(CONFIG_INI)
            self._es = self.config['ES']
        return self._es
