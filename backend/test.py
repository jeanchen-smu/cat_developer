from service.vehicle_score_service import VehicleScoreService

vehicle_score_service = VehicleScoreService()

print vehicle_score_service.get_kpis("2017-06-22", "2017-06-25",[])