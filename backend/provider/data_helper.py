import requests

class Baseride:
     def __init__(self, access_code):
          self.access_code = access_code
          self.vehicle_url = 'http://sg.baseride.com/api/v2/transport/vehicle/?format=json&access_token={}&limit=1000'
          self.position_url = 'http://sg.baseride.com/api/v2/transport/vehicle/{0}/rawgpsdata/position/?format=json&from={1}&to={2}&access_token={3}&raw=True'
     
     def get_vehicle(self): 
          url = self.vehicle_url.format(self.access_code)   
          resp = requests.get(url)
          
          if resp.status_code == 200:
               data = resp.json()
               for rec in data['objects']:
                    yield rec
          else:
               raise StopIteration

     def get_position(self, vehicle_id, from_ts, to_ts):               
          url = self.position_url.format(vehicle_id, from_ts, to_ts, self.access_code)
          resp = requests.get(url)

          if resp.status_code == 200:
               data = resp.json()
               for rec in data['objects']:
                    yield rec
          else:
               raise StopIteration


