from boto3.dynamodb.types import Decimal
from database.base_table import BaseTable
from elasticsearch_dsl import Search, A, Q
from utils.time_helper import TimeHelper


class PositionTable(BaseTable):
    def __init__(self):
        BaseTable.__init__(self, 'POSITION')
        self.tz_help = TimeHelper()

    def insert_position(self, **pos):
        doc = {
            'VehicleID': pos['vehicle_id'],
            'DeviceTS': pos['device_ts'],
            'Lat': pos['lat'],
            'Lon': pos['lon'],
            'Pos': {"lat": pos['lat'], "lon": pos['lon']},
            'Speed': pos['speed'],
            'Direction': pos['bearing'],
            'State': pos['state'],
            'Events': pos['events'],
            'RoadName': pos['road_name'],
            'RoadType': pos['road_type'],
            'SpeedLimit': pos['speed_limit'],
            'OverSpeed': pos['over_speed'],
            'DeviceTS': self.tz_help.convert_local(pos['device_ts'])
        }
        BaseTable.insert(self, str(pos['vehicle_id']) + pos['device_ts'], doc)

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
            .aggs.bucket('VehicleIDs', A('terms', field='VehicleID'))

        resp = dsl.execute()
        for vehicle_id in resp['aggregations']['VehicleIDs']['buckets']:
            yield vehicle_id
