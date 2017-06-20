import psycopg2
from config.config_helper import ConfigHelper


class EnrichHelper:

    def __init__(self):
        params = ConfigHelper().get_enrich_params()

        self.db = psycopg2.connect(
            database=params['Database']['DatabaseName'], user=params['Database']['UserName'],
            password=params['Database']['Password'], host=params['Database']['Host'])
        self.db_cur = self.db.cursor()

        self.query_string = "SELECT name, highway "\
            "FROM planet_osm_roads WHERE ST_DWithin(ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326),3414), way, %s) "\
            "ORDER BY ST_Distance(ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326),3414), way) LIMIT 1"
        self.search_radius = params['SearchRadius']
        self.bad_result = {'road_name': 'NA',
                           'road_type': 'NA', 'speed_limit': 0}

    @staticmethod
    def _get_speed_limit(road_type):
        if road_type == 'NA':
            return 0
        elif road_type in ['motorway', 'motorway_link']:
            return 70
        else:
            return 50

    def enrich_position(self, lat, lon):
        # validate input coordinates
        if (not 0 < lat <= 90) or (not 100 < lon <= 180):
            return self.bad_result

        # query database
        try:
            query = self.query_string % (
                lon, lat, self.search_radius, lon, lat)
            self.db_cur.execute(query)
            result = self.db_cur.fetchone()
            if result:
                return {'road_name': result[0], 'road_type': result[1],
                        'speed_limit': EnrichHelper._get_speed_limit(result[1])}

        except Exception as e:
            print 'Exception - ' + str(e)

        return self.bad_result
