from elasticsearch import Elasticsearch

from . import config


class ESWrapper:
    def __init__(self, config: config.Config):
        self.config = config
        self.client = None

    def init(self):
        api_key = self.config.es.get('es_api_key')
        if api_key and not api_key.startswith("$"):
            self.client = Elasticsearch(
                self.config.es['es_host'],
                api_key=api_key
            )
        else:
            self.client = Elasticsearch(
                self.config.es['es_host'],
                http_auth=(
                    self.config.es['es_user'], self.config.es['es_pass']),
            )

    def create_version_index(self):
        if not self.client.indices.exists(
                index=self.config.es['migration_index']):
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

    def current_version(self):
        hits = self.client.search(index=self.config.es['migration_index'],
                                  query=dict(match_all=dict()),
                                  ignore=[404])['hits']['hits']
        return hits and hits[0]['_source']['version'] or None
