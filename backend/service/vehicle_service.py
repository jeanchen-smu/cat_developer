from database.vehicle_table import VehicleTable
from elasticsearch_dsl import A, Q

class VehicleService(VehicleTable):
    def __init__(self):
        VehicleTable.__init__(self)

    def select_latest_position(self, vehicle_list):
        position_result = []

        vehicle_filter = Q('terms', VehicleID=vehicle_list)
        position_query = Q("constant_score", filter=vehicle_filter)
        position_response = self.get_response(position_query)

        for rec in position_response:
            position = [str(rec['VehicleID']), str(rec['RegistrationNo']), str(rec['Pos']['lon']),
                        str(rec['Pos']['lat']), str(rec['Speed']), str(rec['DeviceTS']), rec['OverSpeed']] 
            position_result.append(position)

        return position_result

    def get_all_vehicles(self):
        vehicle_result = []

        vehicle_query = Q("match_all")
        vehicle_response = self.get_response(vehicle_query)
        
        for rec in vehicle_response:
            vehicle_result.append(str(rec['VehicleID']))
        
        return vehicle_result