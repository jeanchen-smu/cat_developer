from helper.vehicle_score_helper import VehicleScoreHelper
from datetime import datetime, timedelta
import time

score_help = VehicleScoreHelper()

while True:
     date = datetime.today() - timedelta(hours=1)
     score_help.process_score(date, date)
     time.sleep(60*60)
