import os
from configparser import ConfigParser

import typer
from rich import print

from config import Config
from constants import CONFIG_INI
from utils import exceptions

app = typer.Typer()
config = Config()


@app.command(help="Command to initialize Chalan with directory structure")
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

    os.mkdir(config.mig_dir)
    os.mkdir(config.versions)

    print(
        "Please edit configuration/connection/logging "
        "settings in %r before proceeding." % CONFIG_INI
    )
    print("Chalan initialized [green bold]successfully[/green bold]")


@app.command()
def first():
    pass


if __name__ == '__main__':
    app()
