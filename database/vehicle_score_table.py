from database.base_table import BaseTable


class VehicleScoreTable(BaseTable):
    def __init__(self):
        BaseTable.__init__(self, 'VEHICLE_SCORE')

    def insert_vehicle_score(self, **score):
        BaseTable.insert(self, score['Date'] + str(score['VehicleID']), score)
