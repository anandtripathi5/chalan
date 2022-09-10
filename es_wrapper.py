from elasticsearch import Elasticsearch

import config
from utils.exceptions import Exc


class ESWrapper:
    def __init__(self, config: config.Config):
        self.config = config

    def init(self):
        self.client = Elasticsearch(
            self.config.es['es_host'],
            http_auth=(
                self.config.es['es_user'], self.config.es['es_pass']),
        )

    def create_version_index(self):
        if self.client.indices.exists(index=self.config.es['migration_index']):
            Exc(f"Migration index [bold red]{self.config.es['migration_index']}[/bold red] already exists")

        self.client.indices.create(
            index=self.config.es['migration_index'],
            mappings={"properties": {"version": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            }}})
