from service.vehicle_score_service import VehicleScoreService

vehicle_score_service = VehicleScoreService()

print vehicle_score_service.get_stats("2017-06-29", "2017-06-29",None)