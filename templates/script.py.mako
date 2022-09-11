"""${message}
Create Date: ${create_date}
"""
from elasticsearch import Elasticsearch


# revision identifiers, used by Alembic.
revision = ${repr(revision)}
down_revision = ${repr(down_revision)}


def upgrade(es: Elasticsearch):
    ...


def downgrade(es: Elasticsearch):
    ...
