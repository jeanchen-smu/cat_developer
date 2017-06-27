from database.position_table import PositionTable
from database.vehicle_score_table import VehicleScoreTable
from database.vehicle_table import VehicleTable
from config.config_helper import ConfigHelper
from utils.time_helper import TimeHelper


class VehicleScoreHelper:
    def __init__(self):
        config = ConfigHelper()
        score_params = config.get_vehicle_score_params()
        self.data_interval = score_params['SignalInterval']
        self.position_table = PositionTable()
        self.vscore_table = VehicleScoreTable()
        self.vehicle_table = VehicleTable()
        self.time_help = TimeHelper()
        
    def _compute_score(self, vstats):    
        # compute socre of one individual vehicle
        vstats['EngineOffPoints'] = vstats['GPSPoints'] - vstats['EngineOnPoints']
        vstats['IdlingPoints'] = vstats['EngineOnPoints'] - vstats['MovingPoints']
        
        vstats['OverSpeedFrequency'] = 0
        if vstats['MovingPoints'] > 0:
            vstats['OverSpeedFrequency'] = float(vstats['OverSpeedCount']) / float(vstats['MovingPoints'])
        
        vstats['IdlingProportion'] = 0
        if vstats['EngineOnPoints'] > 0:
            vstats['IdlingProportion'] = float(vstats['IdlingPoints']) / float(vstats['EngineOnPoints'])
        
        vstats['EngineOffProportion'] = 0
        if vstats['GPSPoints'] > 0:
            vstats['EngineOffProportion'] = float(vstats['EngineOffPoints']) / float(vstats['GPSPoints'])
    
        vstats['EstimatedDrivingTime'] = vstats['MovingPoints'] * float(self.data_interval)/3600
        vstats['EstimatedDrivingDistance'] = vstats['EstimatedDrivingTime'] * vstats['AverageSpeed']
    
        vstats['Score'] = 1 - vstats['OverSpeedFrequency']
        
        return vstats

    def _get_bad_record(self, vehicle_id, date):
        return {
            'VehicleID': vehicle_id,
            'Date': date,
            'RegistrationNo': 'NA',
            'GPSPoints': 0,
            'EngineOnPoints': 0,
            'EngineOffPoints': 0,
            'IdlingPoints': 0,
            'MovingPoints': 0,
            'OverSpeedCount': 0,
            'OverSpeedFrequency': 0,
            'MaxSpeed': 0,
            'AverageSpeed': 0,
            'IdlingProportion': 0,
            'EngineOffProportion': 0,
            'EstimatedDrivingTime': 0,
            'EstimatedDrivingDistance': 0,
            'Score': 0
        }

    def process_score(self, start_date, end_date):
        # for each vehicle_id in VEHICLES table, compute the score
        # for each day of the given date range
        for vehicle in self.vehicle_table.select_all():
            for date in self.time_help.date_range(start_date, end_date):
                print 'Computing score for {} and date {}'.format(vehicle['VehicleID'], date)
                vstats = self.position_table.vehicle_stats(vehicle['VehicleID'], date)

                if vstats:
                    self.vscore_table.insert_vehicle_score(
                        **self._compute_score(vstats))
                else:
                    self.vscore_table.insert_vehicle_score(
                        **self._get_bad_record(vehicle['VehicleID'], date))
