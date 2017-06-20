import requests


class Baseride:
    def __init__(self):
        base_url = 'http://sg.baseride.com/api/v2'
        self.vehicle_url = base_url + \
            '/transport/vehicle/?format=json&access_token={}&limit=1000'
        self.position_url = base_url + \
            '/transport/vehicle/{0}/rawgpsdata/position/?format=json&from={1}&to={2}&access_token={3}&raw=True'
        self.state_url = base_url + '/transport/vehicle/{0}/rawgpsdata/state/?format=json&from={1}&to={2}&access_token={3}&raw=True'
        self.event_url = base_url + '/transport/vehicle/{0}/rawgpsdata/events/?format=json&from={1}&to={2}&access_token={3}&raw=True'
    
    def get_vehicle(self, access_code): 
        url = self.vehicle_url.format(access_code)   
        resp = requests.get(url)
          
        if resp.status_code == 200:
            data = resp.json()
            for rec in data['objects']:
                yield rec
        else:
            raise StopIteration

    def get_position(self, vehicle_id, start_ts, end_ts, access_code):               
        url = self.position_url.format(vehicle_id, start_ts, end_ts, access_code)
        resp = requests.get(url)

        if resp.status_code == 200:
            data = resp.json()
            for rec in data['objects']:
                yield rec
        else:
            raise StopIteration

    def get_state(self, vehicle_id, start_ts, end_ts, access_code):               
        url = self.state_url.format(vehicle_id, start_ts, end_ts, access_code)
        resp = requests.get(url)

        if resp.status_code == 200:
            data = resp.json()
            for rec in data['objects']:
                yield rec
        else:
            raise StopIteration
    
    def get_event(self, vehicle_id, start_ts, end_ts, access_code):               
        url = self.event_url.format(vehicle_id, start_ts, end_ts, access_code)
        resp = requests.get(url)

        if resp.status_code == 200:
            data = resp.json()
            for rec in data['objects']:
                yield rec
        else:
            raise StopIteration