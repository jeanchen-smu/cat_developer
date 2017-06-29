from database.position_table import PositionTable
from elasticsearch_dsl import A, Q
from config.config_helper import ConfigHelper


class PositionService(PositionTable):
    def __init__(self):
        PositionTable.__init__(self)
        config_helper = ConfigHelper()
        vehicle_score_params = config_helper.get_vehicle_score_params()
        self.start_time = vehicle_score_params['StartTime']
        self.end_time = vehicle_score_params['EndTime']

    def vehicle_stats(self, vehicle_id, date):
        stats = {'Date': date, 'VehicleID': vehicle_id}

        # filters
        vehicle_filter = Q('term', VehicleID=vehicle_id)
        date_filter = Q('term', DeviceTS=date)
        speed_filter = Q('range', Speed={'lt': 1})
        overspeed_filter = Q('range', OverSpeed={'gt': 0})

        # get the position points for this vehicle id & date
        pos_search = self.search.query(Q('constant_score',
                                         filter=vehicle_filter + date_filter))
        stats['GPSPoints'] = pos_search.count()

        # no data for this vehicle id, no need to proceed
        if stats['GPSPoints'] == 0:
            return None

        # get engine on & moving positions
        eng_search = self.search.query(Q('constant_score',
                                         filter=vehicle_filter + date_filter + ~speed_filter))
        stats['EngineOnPoints'] = eng_search.count()
        stats['MovingPoints'] = eng_search.count()

        # get overspeeding positions
        overspeed_search = self.search.query(Q('constant_score',
                                               filter=vehicle_filter + date_filter + overspeed_filter))
        stats['OverSpeedCount'] = overspeed_search.count()

        # get speed stats
        speed_aggs = A('stats', field='Speed')
        speed_dsl = eng_search.extra(
            size=0).aggs.metric('SpeedStats', speed_aggs)
        resp = speed_dsl.execute()
        if resp['aggregations']['SpeedStats']['max'] != None:
            stats['MaxSpeed'] = resp['aggregations']['SpeedStats']['max']
            stats['AverageSpeed'] = resp['aggregations']['SpeedStats']['avg']
        else:
            stats['MaxSpeed'], stats['AverageSpeed'] = 0, 0

        return stats

    def vehicles_by_date(self, start_date, end_date):
        query = Q('constant_score',
                  filter=Q('range', DeviceTS={'from': start_date, 'to': end_date}))
        dsl = self.search\
            .query(query)\
            .extra(size=0)\
            .aggs.metric('VehicleIDs', A('terms', field='VehicleID'))

        resp = dsl.execute()
        for vehicle_id in resp['aggregations']['VehicleIDs']['buckets']:
            yield vehicle_id

    def select_all_position(self, date, vehicle_list):
        position_result = []

        date_filter = Q('range', DeviceTS={'from': date, 'to': date})
        vehicle_filter = Q('terms', VehicleID=vehicle_list)
        position_query = Q(
            "constant_score", filter=date_filter + vehicle_filter)
        position_response = self.get_response(position_query)

        for rec in position_response:
            position_result.append(rec)

        return position_result

    def vehicle_position(self, filter, result):
        must_filters = []
        must_filters.append(
            Q('range', DeviceTS={'gte': filter['start_date'], 'lte': filter['end_date']}))
        if filter['vehicle_list']:
            must_filters.append(Q('terms', VehicleID=filter['vehicle_list']))

        query = Q('bool', must=must_filters)
        pos_search = self.search.query(query).extra(size=5000).source(
            ['Lat', 'Lon', 'Speed', 'VehicleID']
        )
        for rec in pos_search.scan():
            result.append(rec.to_dict())
