from database.parnter_table import PartnerTable
from database.vehicle_table import VehicleTable 
from provider import data_helper

class VehicleDownloader:
     def __init__(self):
          self.partner_table = PartnerTable()
          self.vehicle_table = VehicleTable()
  
     def _reset_account_link_flag(self):
          # unlink all vehicle_table from partner accounts
          for vehicle in self.vehicle_table.select_all():
               self.vehicle_table.update(vehicle['VehicleID'], {'LinkedToAccount': 'N'})

     def start(self):
          self._reset_account_link_flag()
          # get the latest list of partner_table, get the list of
          # vehicle_table belonging to each partner from baseride and upsert
          # vehicle_table table
          for partner in self.partner_table.select_all():
               baseride = data_helper.Baseride(partner['APIAccessCode'])
               for i, vehicle in enumerate(baseride.get_vehicle()):
                    self.vehicle_table.insert_vehicle(api_access_code=partner['APIAccessCode'],
                                                  partner_name=partner['PartnerName'], **vehicle)

               print 'Upserted {} vehicles for {}'.format(i + 1, partner['PartnerName'])
