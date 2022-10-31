# Chalan

Chalan is a migration tool designed and developed for Elasticsearch and
inspired from Alembic

# Installation

```shell
pip install chalan
```

# Initialize

Setup migration tool, configuration files and migration folders using below
command

```shell
chalan init
```

This will create a directory `es_migrations/versions` that will have all the
migrations file and `chalan.ini` that will contain all the configuration of the
migration tools

```bash
--- es_migrations/
  |
  --versions/
--- chalan.ini
```

# Create Revision

Create revision file with migration changes in version directory with below
command.

```shell
chalan revision -m"<some message>"
```

Above command will create a migration file under `versions/` folder with
upgrade and downgrade function. That will help in upgrade/downgrade of the
migration tool.

# Upgrade

Command used to upgrade the migration level to head(current level). Or you can
also specify specific version where you want upgrade the version to.

```shell
chalan upgrade
# or
chalan upgrade <specific version>
```

# Downgrade

Command used to downgrade the migration level to base(initial version). Or
specify the level you want to downgrade to.

```shell
chalan downgrade # Downgrade 1 level down
# or
chalan downgrade --version base # Downgrade to base version
```