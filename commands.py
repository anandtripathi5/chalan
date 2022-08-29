import os

import typer
from rich import print

from utils import exceptions

app = typer.Typer()


@app.command(help="Command to initialize vahana with directory structure")
def init(directory: str = 'es_migrations') -> None:
    """
    Initialize a new scripts directory.
    :param config: a :class:`.Config` object.
    :param directory: string path of the target directory
    """

    if os.access(directory, os.F_OK) and os.listdir(directory):
        raise exceptions.CommandError(
            "Directory %s already exists" % directory
        )

    if not os.access(directory, os.F_OK):
        print()

    versions = os.path.join(directory, "versions")
    print(
        "[bold green]Creating[/bold green] directory "
        "[blue]es_migrations[/blue] :file_folder:!"
    )

    util.msg(
        "Please edit configuration/connection/logging "
        "settings in %r before proceeding." % config_file
    )
