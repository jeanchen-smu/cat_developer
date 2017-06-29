# from service.vehicle_score_service import VehicleScoreService

# vehicle_score_service = VehicleScoreService()

# print vehicle_score_service.get_stats("2017-06-29", "2017-06-29",None)

# def to_date(date_string):
#     return date_string.split("T")[0]

# print to_date()

filter = {
        'start_date': "2017-06-22",
        'end_date': "2017-06-22",
        'vehicle_list': [29875, 29873]
        }

from service.position_service import PositionService

position_service = PositionService()

print position_service.get_trips(filter)
