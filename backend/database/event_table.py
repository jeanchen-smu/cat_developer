from database.base_table import BaseTable


class EventTable(BaseTable):
    def __init__(self):
        BaseTable.__init__(self, 'EVENT')

    def insert_event(self, vehicle_id, device_ts, event_list):
        key = str(vehicle_id) + device_ts
        doc = {
            'VehicleID': vehicle_id,
            'DeviceTS': device_ts,
            'Events': event_list
        }
        BaseTable.insert(self, key, doc)

    def insert_event_bulk(self, vehicle_id, events):
        docs = (
            {
                '_index': self.index,
                '_type': self.doc_type,
                '_id': str(vehicle_id) + device_ts,
                'VehicleID': vehicle_id,
                'DeviceTS': device_ts,
                'Events': event_list
            }
            for device_ts, event_list in events.iteritems()
        )
        BaseTable.insert_bulk(self, docs)
