from database.app_user_table import AppUserTable

class AppUserService(AppUserTable):
    def __init__(self):
        AppUserService.__init__(self)

    def get_vehicles_by_username(self, username):
        vehicle_list=[]
        vehicles_by_username_query = Q('match', UserName=username)
        for response in self.get_response(vehicles_by_username_query):
            vehicle_id.append(response['VehicleID'])
        
        return vehicle_list