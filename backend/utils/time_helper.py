from dateutil.parser import parse
from datetime import datetime, timedelta
import pytz


class TimeHelper:
    def __init__(self):
        self.local_tz = pytz.timezone('Singapore')
        self.utc_tz = pytz.utc
        self.DT_UTC_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
        self.DT_LZ_FORMAT = '%Y-%m-%dT%H:%M:%S.%f+08:00'
        self.D_UTC_FORMAT = '%Y-%m-%d'
        self.D_LZ_FORMAT = '%Y-%m-%d'

    def convert_local(self, utc_time):
        return parse(utc_time)\
            .astimezone(self.local_tz)\
            .strftime(self.DT_LZ_FORMAT)

    def convert_utc(self, local_time):
        return parse(local_time)\
            .astimezone(self.utc_tz)\
            .strftime(self.DT_UTC_FORMAT)
    
    def parse_ts(self, ts_str):
        return parse(ts_str)

    def utc_now(self, minus_seconds=0):
        if minus_seconds == 0:
            return datetime.utcnow().strftime(self.DT_UTC_FORMAT)
        return (datetime.utcnow() - timedelta(seconds=minus_seconds))\
            .strftime(self.DT_UTC_FORMAT)

    def today(self, minus_days=0):
        if minus_days == 0:
            return datetime.today().strftime(self.D_LZ_FORMAT)
        return (datetime.today() - timedelta(minus_days))\
            .strftime(self.D_LZ_FORMAT)
    
    def utc_today(self, minus_days=0):
        if minus_days == 0:
            return datetime.utcnow().strftime(self.D_UTC_FORMAT)
        return (datetime.utcnow() - timedelta(minus_days))\
            .strftime(self.D_UTC_FORMAT)    

    def date_range(self, start_date, end_date):
        for day in range((end_date - start_date).days + 1):
            yield (start_date + timedelta(day)).strftime(self.D_LZ_FORMAT)
