from downloader.download_position import PositionDownloader
import time

pos_downloader = PositionDownloader()
while (True):
   pos_downloader.start(use_lambda=True)
   time.sleep(30)
