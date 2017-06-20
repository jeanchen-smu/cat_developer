from database.base_table import BaseTable
from utils.time_helper import TimeHelper

class VehicleTable(BaseTable):
    def __init__(self):
        BaseTable.__init__(self, 'VEHICLE')
        self.tz_help = TimeHelper()

    def upsert_vehicle(self, **vehicle):
        doc = {
            'VehicleID': vehicle['id'],
            'RegistrationNo': vehicle['registration_code'],
            'Details': vehicle['full_name'],
            'VehicleType': vehicle['kind'],
            'OwnerName': vehicle['park_info']['enterprise_info']['name'],
            'LinkedToAccount': 'Y',
            'APIAccessCode': vehicle['api_access_code'],
            'PartnerName': vehicle['partner_name'],
            'Lat': vehicle['position']['lat'],
            'Lon': vehicle['position']['lon'],
            'Pos': {"lat": vehicle['position']['lat'], "lon": vehicle['position']['lon']},
            'Speed': vehicle['position']['speed'],
            'Direction': vehicle['position']['bearing'],
            'RoadName': vehicle['position']['road_name'],
            'RoadType': vehicle['position']['road_type'],
            'SpeedLimit': vehicle['position']['speed_limit'],
            'OverSpeed': vehicle['position']['over_speed'],
            # 'State': {
            #     'IgnitionStatus': 'ON' if vehicle['inputs']['engine_on'] else 'OFF',
            #     'BatteryVolt': vehicle['inputs']['power_voltage'],
            # },
            'DeviceTS': self.tz_help.convert_local(vehicle['position']['device_ts'])
        }
        BaseTable.insert(self, vehicle['id'], doc)