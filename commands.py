import os
from configparser import ConfigParser

import typer
from rich import print

from config import Config
from constants import CONFIG_INI
from es_wrapper import ESWrapper
from migrate import Migrate
from utils import exceptions

app = typer.Typer(rich_markup_mode="rich")
config = Config()
es = ESWrapper(config)
migrate = Migrate(es, config)


@app.command(
    help="Command to initialize [green bold]Chalan[/green bold] with directory structure")
def init() -> None:
    """
    Initialize a new scripts directory.
    """
    config.create_ini()

    if os.access(config.mig_dir, os.F_OK) and os.listdir(config.mig_dir):
        print("Directory %s already exists" % config.mig_dir)

    print(
        "[bold green]Creating[/bold green] directory "
        "[blue]es_migrations[/blue] :file_folder:!"
    )
    os.makedirs(config.mig_dir, exist_ok=True)
    os.makedirs(config.versions, exist_ok=True)
    print(
        "Please edit configuration/connection/logging "
        "settings in %r before proceeding." % CONFIG_INI
    )
    print('''Chalan setup [green bold]completed[/green bold] :green_heart: \nAfter editing the configuration file then go ahead and create first revision with revision command
    ''')


@app.command(
    help="Command to generate [green bold]migration file[/green bold]")
def revision(message: str = typer.Option(..., "--message", "-m",
                                         help="message will be part of the migration file name")):
    migrate.create_revision(message=message)


if __name__ == '__main__':
    app()
