from database.position_table import PositionTable
from database.vehicle_table import VehicleTable
from database.event_table import EventTable
from provider.data_helper import Baseride
from helper.enrich_helper import EnrichHelper
from utils.time_helper import TimeHelper


class PositionDownloader:
    def __init__(self):
        self.position_table = PositionTable()
        self.vehicle_table = VehicleTable()
        self.event_table = EventTable()
        self.baseride = Baseride()
        self.enricher = EnrichHelper()
        self.time_help = TimeHelper()
        
    def _enrich(self, pos):
        if pos['speed'] == 0:  # don't enrich 0 speed points
            pos.update({'road_name': 'NA', 'road_type': 'NA',
                        'speed_limit': 0, 'over_speed': 0})
        else:
            resp = self.enricher.enrich_position(pos['lat'], pos['lon'])
            # compute overspeeding
            resp['over_speed'] = 0
            if resp['speed_limit'] != 0:
                resp['over_speed'] = pos['speed'] - resp['speed_limit']
            pos.update(resp)

    def _get_state(self, args, states):
        for state in self.baseride.get_state(**args):
            try:
                if state['inputs'].has_key('analog'): #new device
                    battery_volt = float(state['inputs']['analog']['1']) * 0.1176470588235
                    ignition_status = 'ON' if state['inputs']['logical']['io_status']['ignition_port'] else 'OFF'
                else: #old 3g device
                    battery_volt = None
                    if state['inputs'].has_key('power_voltage'):
                        battery_volt = float(state['inputs']['power_voltage'])
                    ignition_status = 'ON' if state['inputs']['engine_on'] else 'OFF'

                states[state['device_ts']] = {
                    'BatteryVolt': battery_volt,
                    'IgnitionStatus': ignition_status
                }
            except Exception as e:
                print 'Exception - _get_state', e

    def _get_event(self, args, events):
        for event in self.baseride.get_event(**args):
            try:
                if not events.has_key(event['device_ts']):
                    events[event['device_ts']] = []
                events[event['device_ts']].append(event['events'])
            except:
                print 'Exception - _get_event', e
    
    def _fetch_position(self, args):
        states, events = {}, {}
        # get data from state & events api
        self._get_state(args, states)
        self._get_event(args, events)

        #insert events -- for testing to see any event timestamp that doesn't have
        #a corresponding position time stamp
        for device_ts, event_list in events.iteritems():
            self.event_table.insert_event(args['vehicle_id'], device_ts, event_list)

        # get data from position api
        for pos in self.baseride.get_position(**args):
            # enrich with road name, speed limit etc.
            self._enrich(pos)
            # merge with state & events
            pos['state'] = None
            if states.has_key(pos['device_ts']):
                pos['state'] = states[pos['device_ts']]

            pos['events'] = None
            if events.has_key(pos['device_ts']):
                pos['events'] = events[pos['device_ts']]
           
            # insert to position table
            self.position_table.insert_position(**pos)

    def start(self, start_ts, end_ts, max_vehicles):
        #convert to utc time
        start_ts_utc = self.time_help.convert_utc(start_ts)
        end_ts_utc = self.time_help.convert_utc(end_ts)

        # for each active vehicle from VEHICLES table,
        # get the position data
        for index, vehicle in enumerate(self.vehicle_table.select_all()):
            if vehicle['LinkedToAccount'] == 'N':
                continue
                
            if max_vehicles and index > max_vehicles:  # for testing purpose, to limit the download
                break
            print 'Fetching position data for vehicle {}'.format(vehicle['VehicleID'])

            args = {}
            args['vehicle_id'] = vehicle['VehicleID']
            args['start_ts'] = start_ts_utc
            args['end_ts'] = end_ts_utc
            args['access_code'] = vehicle['APIAccessCode']
            self._fetch_position(args)
