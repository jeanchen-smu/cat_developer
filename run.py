from database import setup
from database.vehicle_table import VehicleTable
from database.position_table import PositionTable
from database.parnter_table import PartnerTable
from downloader.download_vehicle import VehicleDownloader
from downloader.download_position import PositionDownloader
from helper.vehicle_score_helper import VehicleScoreHelper
from datetime import datetime, timedelta

#initialize connection to elastic search
es = setup.es

# #delete all existing tables
setup.delete_all_tables()
setup.create_tables()

# #create partners
partner = PartnerTable()
partner.insert( 'Goldbell', {'PartnerName': 'Goldbell', 'APIAccessCode': '3e399a6b6a'})
es.indices.refresh(index='_all')

# #fetch details of vehicles belonging to partners
VehicleDownloader().start()
es.indices.refresh(index='_all')
# #refresh the index
# #es.indices.refresh()

# #get gps data for all active vehicles'''
#PositionDownloader().start()
#es.indices.refresh(index='_all')

##export data for validation
#position_table = PositionTable()
#position_table.export('position.json')

#compute driving scores for vehicles
#score_help = VehicleScoreHelper()
#yesterday = datetime.today() - timedelta(1)
#today = datetime.today()
#score_help.process_score(today, today)





