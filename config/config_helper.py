import yaml


class ConfigHelper:
    def __init__(self):
        with open(r'./config/config.yaml', 'r') as fp:
            config = yaml.load(fp.read())
        self.active_config = config[config['ActiveConfig']]

    def get_es_params(self):
        return self.active_config['ElasticSearch']

    def get_lambda_params(self):
        return self.active_config['Lambda']

    def get_enrich_params(self):
        return self.active_config['Enrich']

    def get_vehicle_score_params(self):
        return self.active_config['VehicleScore']
