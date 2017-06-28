from config.config_helper import ConfigHelper
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import scan, bulk
from requests_aws4auth import AWS4Auth
from elasticsearch_dsl import Search

class BaseTable:
    def __init__(self, doc_type):
        self.config_helper = ConfigHelper()

        es_params = self.config_helper.get_es_params()
        self._init_es(es_params)
        self.index = es_params['Index']
        self.doc_type = doc_type

        self.search = Search(using=self.es, index=self.index,
                             doc_type=self.doc_type)

    def _init_es(self, es_params):
        if es_params['Host'] == 'localhost':
            self.es = Elasticsearch()
        else:
            self.es = Elasticsearch(
                hosts=[{'host': es_params['Host'], 'port': es_params['Port']}],
                http_auth=AWS4Auth(
                    es_params['AccessKeyID'], es_params['AccessKey'], es_params['Region'], 'es'),
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection
            )

    def insert(self, id, doc):
        res = self.es.index(
            index=self.index,
            doc_type=self.doc_type,
            id=id,
            body=doc
        )
        return res['created']
    
    def insert_bulk(self, docs):
        return bulk(self.es, docs)

    def update(self, id, doc):
        res = self.es.update(
            index=self.index,
            doc_type=self.doc_type,
            id=id,
            body={"doc": doc} #partial updates
        )

    def select_all(self):
        for rec in scan(self.es,
                        query={"query": {"match_all": {}}},
                        index=self.index, doc_type=self.doc_type,
                        request_timeout=30*60):
            yield rec['_source']

    def export(self, file_name):
        with open(file_name, 'w') as fp:
            for rec in self.select_all():
                fp.write(str(rec) + '\n')

    def get_response(self, statement):
        for rec in self.search.query(statement).scan():
            yield rec.to_dict()    
    