from database.position_table import PositionTable
from database.vehicle_table import VehicleTable
from database.event_table import EventTable
from provider.data_helper import Baseride
from helper.enrich_helper import EnrichHelper
from utils.time_helper import TimeHelper
from threading import Thread
import time

class DownloadWorker(Thread):
    def __init__(self, args):
        Thread.__init__(self)

        self.args = args
        self.position_table = PositionTable()
        self.vehicle_table = VehicleTable()
        self.event_table = EventTable()
        self.baseride = Baseride()
        self.enricher = EnrichHelper()

        self.position, self.states, self.events = [], {}, {}
        self._get_position()
        self._get_state()
        self._get_event()
        print 'Position-{}, States-{}, Events-{}'.format(
            len(self.position), len(self.states), len(self.events))

    def _get_position(self):
        for pos in self.baseride.get_position(**self.args):
            self.position.append(pos)

    def _get_state(self):
        for state in self.baseride.get_state(**self.args):
            try:
                inputs = state.get('inputs', None)
                if not inputs:
                    continue

                # cellocator device, Cello.MCG, Cello.CSA etc.
                if inputs.get('@', None):
                    battery_volt = inputs.get('analog', {}).get('1', None)
                    battery_const = 0.1176470588235
                    ignition_status = inputs.get('logical', {})\
                        .get('io_status', {}).get('ignition_port', None)

                else:  # old 3g device
                    battery_volt = inputs.get('power_voltage', None)
                    battery_const = 1
                    ignition_status = inputs.get('engine_on', None)

                # standardize the field values
                if battery_volt:
                    battery_volt = float(battery_volt) * battery_const
                if ignition_status:
                    ignition_status = 'ON' if ignition_status else 'OFF'

                # add state @ timestamp to array
                self.states[state['device_ts']] = {
                    'BatteryVolt': battery_volt,
                    'IgnitionStatus': ignition_status
                }
            except Exception as e:
                print 'Exception - _get_state', e

    def _get_event(self):
        for event in self.baseride.get_event(**self.args):
            try:
                if not self.events.has_key(event['device_ts']):
                    self.events[event['device_ts']] = []
                self.events[event['device_ts']].append(event['events'])
            except Exception as e:
                print 'Exception - _get_event', e

    def _enrich(self, pos):
        if pos['speed'] == 0:  # don't enrich 0 speed points
            pos.update({
                'road_name': 'NA',
                'road_type': 'NA',
                'speed_limit': 0,
                'over_speed': 0
            })
        else:
            resp = self.enricher.enrich_position(pos['lat'], pos['lon'])
            # compute overspeeding
            resp['over_speed'] = 0
            if resp['speed_limit'] != 0:
                resp['over_speed'] = pos['speed'] - resp['speed_limit']
            pos.update(resp)

    def  run(self):
        print 'Starting vehicle {}'.format(self.args['vehicle_id'])
        #insert to events tables
        self.event_table.insert_event_bulk(self.args['vehicle_id'], self.events)
        
        #enrich position
        for pos in self.position:
            self._enrich(pos)
            # merge with state & events
            pos['state'] = None
            if self.states.has_key(pos['device_ts']):
                pos['state'] = self.states[pos['device_ts']]

            pos['events'] = None
            if self.events.has_key(pos['device_ts']):
                pos['events'] = self.events[pos['device_ts']]

         # insert to position table
        self.position_table.insert_position_bulk(self.position)
        print 'Done vehicle {}'.format(self.args['vehicle_id'])
    
class PositionDownloader:
    def __init__(self, max_workers=10):
        self.max_workers = max_workers
        self.vehicle_table = VehicleTable()
        self.time_help = TimeHelper()

    def _prepare_args(self, vehicle, start_date, end_date):
        args = {}

        args['start_ts'] = self.time_help.convert_utc(
            start_date.strftime(self.time_help.D_LZ_FORMAT) +
            'T00:00:00.000+08:00'
        )
        args['end_ts'] = self.time_help.convert_utc(
            end_date.strftime(self.time_help.D_LZ_FORMAT) +
            'T23:59:59.999+08:00'
        )
        args['vehicle_id'] = vehicle['VehicleID']
        args['access_code'] = vehicle['APIAccessCode']
        return args

    def start(self, start_date, end_date, max_vehicles=None):
        # for each active vehicle from VEHICLES table,
        # get the position data
        workers = []
        for index, vehicle in enumerate(self.vehicle_table.select_all()):
            # if the vehicle is not linked to the account, ignore it
            if vehicle['LinkedToAccount'] == 'N':
                continue
            if max_vehicles and index > max_vehicles:  # for testing purpose, to limit the download
                break
        
            print 'Fetching position data for vehicle {}'.format(
                vehicle['VehicleID'])

            # start worker threads for parallel  processing
            args = self._prepare_args(vehicle, start_date, end_date)
            worker = DownloadWorker(args) # create worker object (downloads data)
            worker.start()
            workers.append(worker)

            # control parallel processing
            while len(workers) >= self.max_workers:
                print 'Max-workers {} reached'.format(len(workers))
                for i, worker in enumerate(workers): # remove finished workers
                    if not worker.is_alive():
                        del workers[i]
                time.sleep(5) # wait for 5 secs

        # wait for all workers to finish
        for worker in workers:
            worker.join()


