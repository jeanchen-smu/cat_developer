from database.base_table import BaseTable
from utils.time_helper import TimeHelper

class VehicleTable(BaseTable):
    def __init__(self):
        BaseTable.__init__(self, 'VEHICLE')
        self.tz_help = TimeHelper()

    def insert_vehicle(self, **vehicle):
        doc = {
            'VehicleID': vehicle['id'],
            'RegistrationNo': vehicle['registration_code'],
            'Details': vehicle['full_name'],
            'VehicleType': vehicle['kind'],
            'OwnerName': vehicle['park_info']['enterprise_info']['name'],
            'LinkedToAccount': 'Y',
            'APIAccessCode': vehicle['api_access_code'],
            'PartnerName': vehicle['partner_name']
        }
        BaseTable.insert(self, vehicle['id'], doc)

    def update_latest_position(self, **pos):
        doc = {
            'Lat': pos['lat'],
            'Lon': pos['lon'],
            'Pos': {"lat": pos['lat'], "lon": pos['lon']},
            'Speed': pos['speed'],
            'Direction': pos['bearing'],
            'RoadName': pos['road_name'],
            'RoadType': pos['road_type'],
            'SpeedLimit': pos['speed_limit'],
            'OverSpeed': pos['over_speed'],
            'DeviceTS': self.tz_help.convert_local(pos['device_ts'])
        }
        BaseTable.update(self, pos['vehicle_id'], doc)
