import os

import typer
from rich import print

from .config import Config
from .constants import CONFIG_INI
from .es_wrapper import ESWrapper
from .migrate import Migrate

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


@app.command(
    help="Command to upgrade [green bold]migration version[/green bold]")
def upgrade(version: str = typer.Option("head",
                                        help="If not version provided then upgrade to latest version else upgrade to specific version",
                                        )):
    migrate.upgrade(version)
    print("Chalan [green bold]successful[/green bold].")


@app.command(
    help="Command to downgrade [green bold]migration version[/green bold]")
def downgrade(version: str = typer.Option(None,
                                          help="downgrade to specific version. Specify 'base' to migrate to initial version",
                                          ), level: int = typer.Option(1,
                                                                       help="downgrade number of level down")):
    if version == 'base':
        level = -1
    migrate.downgrade(version, level)
    print("Chalan [green bold]successful[/green bold].")


if __name__ == '__main__':
    app()
