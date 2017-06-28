from database import setup
from database.vehicle_table import VehicleTable
from database.position_table import PositionTable
from database.parnter_table import PartnerTable
from downloader.download_vehicle import VehicleDownloader
from downloader.download_position import PositionDownloader
from helper.vehicle_score_helper import VehicleScoreHelper
from datetime import datetime, timedelta
from utils.time_helper import TimeHelper


#initialize connection to elastic search
es = setup.es

#delete all existing tables
#setup.delete_all_tables()
#setup.create_tables()

 #create partners
#partner = PartnerTable()
#partner.insert( 'Goldbell', {'PartnerName': 'Goldbell', 'APIAccessCode': 'e62a48f233'})
# partner.insert( 'Goldbell', {'PartnerName': 'Goldbell', 'APIAccessCode': '1009b9a70c'})
#es.indices.refresh(index='_all')

# # #fetch details of vehicles belonging to partners
#VehicleDownloader().start()
#es.indices.refresh(index='_all')

#get gps data for all active vehicles
tz_help = TimeHelper()
yesterday = tz_help.today(minus_days=1)
start_ts = yesterday + "T00:00:00.000+08:00"
end_ts = yesterday + "T23:59:59.999+08:00"

PositionDownloader().start(start_ts, end_ts, 5)
es.indices.refresh(index='_all')

##export data for validation
#position_table = PositionTable()
#position_table.export('position.json')

#compute driving scores for vehicles
score_help = VehicleScoreHelper()
yesterday = datetime.today() - timedelta(1)
#today = datetime.today()
#score_help.process_score(yesterday, yesterday)





