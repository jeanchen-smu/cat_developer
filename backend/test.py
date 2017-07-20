from config.config_helper import ConfigHelper
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import scan, bulk
from requests_aws4auth import AWS4Auth
from elasticsearch_dsl import Search

es = es_search =  None
def init_es():
        config_helper = ConfigHelper()

        es_params = config_helper.get_es_params()
        index = es_params['Index']
        doc_type = 'POSITION'

        if es_params['Host'] == 'localhost':
                es = Elasticsearch()
        else:
                es = Elasticsearch(
                        hosts=[{'host': es_params['Host'], 'port': es_params['Port']}],
                        http_auth=AWS4Auth(
                                es_params['AccessKeyID'], es_params['AccessKey'], es_params['Region'], 'es'),
                        use_ssl=True,
                        verify_certs=True,
                        timeout = 5*60,
                        connection_class=RequestsHttpConnection
                )
        es_search = Search(using=es, index=index,
                        doc_type=doc_type)


init_es()


es.



