import boto3
from config.config_helper import ConfigHelper
from database.vehicle_table import VehicleTable
import lambda_position
from datetime import datetime, timedelta
from dateutil.parser import parse
from utils.time_helper import TimeHelper
import json


class PositionDownloader:
    def __init__(self):
        self.vehicle_table = VehicleTable()
        lambda_params = ConfigHelper().get_lambda_params()
        self.aws_lambda = boto3.client(
            'lambda',
            aws_access_key_id=lambda_params['AccessKeyID'],
            aws_secret_access_key=lambda_params['AccessKey'],
            region_name=lambda_params['Region']
        )
        self.tz_help = TimeHelper()

    def _prepare_lambda_args(self, vehicle):
        lambda_args = {}
        if vehicle.has_key('DeviceTS'):
            last_device_ts = self.tz_help.convert_utc(vehicle['DeviceTS'])
        else:
            # first time when a vehicle is appearing
            last_device_ts = self.tz_help.utc_now(minus_seconds=30)

        lambda_args['VehicleID'] = vehicle['VehicleID']
        lambda_args['DeviceTS'] = last_device_ts
        lambda_args['APIAccessCode'] = vehicle['APIAccessCode']
        return lambda_args

    def start(self, use_lambda=False):
        # for each active vehicle from VEHICLES table,
        # get the raw position data
        for vehicle in self.vehicle_table.select_all():
            if vehicle['LinkedToAccount'] == 'N':
                continue

            print 'Fetching position data for vehicle {}'.format(vehicle['VehicleID'])

            # prepare arguments to lambda function
            lambda_args = self._prepare_lambda_args(vehicle)

            if use_lambda:
                response = self.aws_lambda.invoke_async(
                    FunctionName='fetch_position',
                    InvokeArgs=json.dumps(lambda_args)
                )
                # add logging
            else:
                lambda_position.fetch_position(lambda_args, None)
