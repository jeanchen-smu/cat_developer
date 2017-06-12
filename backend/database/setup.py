import yaml
from config.config_helper import ConfigHelper
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

config = ConfigHelper()
es_params = config.get_es_params()
if es_params['Host'] == 'localhost':
     es = Elasticsearch()
else:
     es = Elasticsearch(
          hosts=[{'host': es_params['Host'], 'port': es_params['Port']}],
          http_auth=AWS4Auth(
               es_params['AccessKeyID'], es_params['AccessKey'], es_params['Region'], 'es'),
          use_ssl=True,
          verify_certs=True,
          connection_class=RequestsHttpConnection
     )


def delete_all_tables():
    es.indices.delete(index='_all')
    
def create_tables():
    with open(r'./database/schema.yaml', 'r') as fp:
        schema =  yaml.load(fp.read())

    mappings={}
    for doc_type in schema.keys():
        mappings[doc_type] = {'properties':{}}
        for field in schema[doc_type]:
            mappings[doc_type]['properties'][field.keys()[0]] = {'type': field[field.keys()[0]]}

    es_params = config.get_es_params()
    es.indices.create(index=es_params['Index'], body={'mappings': mappings})
