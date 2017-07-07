from database import setup
from database.vehicle_table import VehicleTable
from database.position_table import PositionTable
from database.parnter_table import PartnerTable
from downloader.download_vehicle import VehicleDownloader
from downloader.download_position import PositionDownloader
from helper.vehicle_score_helper import VehicleScoreHelper
from datetime import datetime, timedelta, date
from utils.time_helper import TimeHelper

# initialize
es = setup.es

vehicle_downloader = VehicleDownloader()
position_downloader = PositionDownloader()
score_helper = VehicleScoreHelper()


def _get_date_tuples(start_date, end_date, step):
    date_tuples, start, end = [], start_date, start_date
    while start <= end_date:
        end = min(start + timedelta(step), end_date)
        date_tuples.append((start, end))
        start = end + timedelta(1)
    return date_tuples


def download_historic_positions(start_date, end_date, step=7):
    date_tuples = _get_date_tuples(start_date, end_date, step)
    for (start, end) in date_tuples:
        print 'Downloading data for range ', start, end
        # download position data
        position_downloader.start(start, end)
        # compute scores
        score_helper.process_score(start, end)


if __name__ == '__main__':
    # vehicle_downloader.start()
    # es.indices.refresh(index='_all')
    end = datetime.today() - timedelta(1)
    start = end
    download_historic_positions(start.date(), end.date())
