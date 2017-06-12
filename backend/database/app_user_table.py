from base_table import BaseTable

class AppUserTable(BaseTable):
    def __init__(self):
        BaseTable.__init__(self, 'APPUSER')
    
    def insert_app_user(self, **user):
        BaseTable.insert(self,  (pos['UserName'])+str(pos['VehicleID'], user)
