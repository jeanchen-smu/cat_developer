from service.vehicle_score_service import VehicleScoreService

vehicle_score_service = VehicleScoreService()

print vehicle_score_service.get_rank("2017-06-29", "2017-06-29")

# def to_date(date_string):
#     return date_string.split("T")[0]

# print to_date()

# from service.position_service import PositionService

# position_service = PositionService()