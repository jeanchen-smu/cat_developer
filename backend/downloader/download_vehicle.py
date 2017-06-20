from database.parnter_table import PartnerTable
from database.vehicle_table import VehicleTable
from provider.data_helper import Baseride
from helper.enrich_helper import EnrichHelper


class VehicleDownloader:
    def __init__(self):
        self.partner_table = PartnerTable()
        self.vehicle_table = VehicleTable()
        self.baseride = Baseride()
        self.enricher = EnrichHelper()

    def _reset_account_link_flag(self):
        # unlink all vehicle_table from partner accounts
        for vehicle in self.vehicle_table.select_all():
            self.vehicle_table.update(vehicle['VehicleID'], {
                'LinkedToAccount': 'N'})

    def _enrich(self, pos):
        if pos['speed'] == 0:  # don't enrich 0 speed points
            pos.update({'road_name': 'NA', 'road_type': 'NA',
                        'speed_limit': 0, 'over_speed': 0})
        else:
            resp = self.enricher.enrich_position(
                float(pos['lat']), float(pos['lon']))
            # compute overspeeding
            resp['over_speed'] = 0
            if resp['speed_limit'] != 0:
                resp['over_speed'] = pos['speed'] - resp['speed_limit']
            pos.update(resp)

    def start(self):
        self._reset_account_link_flag()
        # get the latest list of partner_table, get the list of
        # vehicle_table belonging to each partner from baseride and upsert
        # vehicle_table table
        for partner in self.partner_table.select_all():
            for index, vehicle in enumerate(self.baseride.get_vehicle(partner['APIAccessCode'])):
                try:
                    self._enrich(vehicle['position'])
                    self.vehicle_table.upsert_vehicle(api_access_code=partner['APIAccessCode'],
                                                      partner_name=partner['PartnerName'], **vehicle)
                except:
                    print 'Exception while processing - ', vehicle['id']

            if index:
                print 'Upserted {} vehicles for {}'.format(index + 1, partner['PartnerName'])
