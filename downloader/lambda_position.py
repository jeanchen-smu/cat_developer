from database.position_table import PositionTable
from database.vehicle_table import VehicleTable
from provider.data_helper import Baseride
from helper.enrich_helper import EnrichHelper
from utils.time_helper import TimeHelper


class FetchHelper:
    def __init__(self, args):
        self.args = args
        self.position_table = PositionTable()
        self.vehicle_table = VehicleTable()
        self.baseride = Baseride(self.args['APIAccessCode'])
        self.enricher = EnrichHelper()
        self.tz_help = TimeHelper()

    def _enrich(self, pos):
        if pos['speed'] == 0:  # don't enrich 0 speed points
            pos.update({'road_name': 'NA', 'road_type': 'NA',
                        'speed_limit': 0, 'over_speed': 0})
        else:
            resp = self.enricher.enrich_position(pos['lat'], pos['lon'])
            # compute overspeeding
            resp['over_speed'] = 0
            if resp['speed_limit'] != 0:
                resp['over_speed'] = pos['speed'] - resp['speed_limit']
            pos.update(resp)

    def fetch_position(self):
        last_device_ts = self.tz_help.parse_ts(self.args['DeviceTS'])
        last_pos = None
        for pos in self.baseride.get_position(self.args['VehicleID'], self.args['DeviceTS'],
                                              self.tz_help.utc_now()):

            self._enrich(pos)  # enrich with road name, speed limit etc.
            self.position_table.insert_position(**pos)  # insert to position table

            # find the latest record
            device_ts = self.tz_help.parse_ts(pos['device_ts'])
            if device_ts >= last_device_ts:
                last_pos = pos
                last_device_ts = device_ts

        # update VEHICLE table with the latest gps point
        if last_pos != None:
            self.vehicle_table.update_latest_position(**last_pos)

#lambda entry point
def fetch_position(args, context):
    fetch_help = FetchHelper(args)
    fetch_help.fetch_position()
