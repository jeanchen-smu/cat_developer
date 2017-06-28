from database.vehicle_score_table import VehicleScoreTable
from elasticsearch_dsl import A, Q
from config.config_helper import ConfigHelper


class VehicleScoreService(VehicleScoreTable):
    def __init__(self):
        VehicleScoreTable.__init__(self)
        config_helper = ConfigHelper()
        self.vehicle_score_params = config_helper.get_vehicle_score_params()
        self.start_time = self.vehicle_score_params['StartTime']
        self.end_time = self.vehicle_score_params['EndTime']

    def get_lastest_date(self):
        latest_date_aggs = A('max', field="Date")
        latest_date_search = self.search.query().extra(
            size=0).aggs.metric("LatestDate", latest_date_aggs)
        latest_date_response = latest_date_search.execute()

        return latest_date_response['aggregations']['LatestDate']['value_as_string']

    def select_score_by_date_range(self, start_date, end_date, vehicle_list):
        score_result = []

        date_filter = Q('range', Date={'from': start_date, 'to': end_date})
        vehicle_filter = Q('terms', VehicleID=vehicle_list)
        score_query = Q("constant_score", filter=date_filter + vehicle_filter)
        score_response = self.get_response(score_query)

        for rec in score_response:
            score_result.append(rec)

        return score_result

    def select_active_vehicle_score(self, start_date, end_date, vehicle_list):
        min_active_time = self.vehicle_score_params['MinActiveTime']

        score_result = []

        date_filter = Q('range', Date={
                        'gte': start_date + self.start_time, 'lte': end_date + self.end_time})
        vehicle_filter = Q('terms', VehicleID=vehicle_list)
        active_filter = Q('range', EstimatedDrivingTime={
                          'gte': min_active_time})
        active_query = Q("constant_score", filter=date_filter +
                         vehicle_filter + active_filter)

        card_aggs = A('cardinality', field="VehicleID")
        active_count_query = self.search.query(active_query).extra(
            size=0).aggs.metric('VehicleCount', card_aggs)

        active_score_count = active_count_query.execute(
        )['aggregations']['VehicleCount']['value']
        total_score_count = len(vehicle_list)

        score_response = self.get_response(active_query)

        for rec in score_response:
            score_result.append(rec)

        return score_result, active_score_count, total_score_count

    def get_kpis(self, start_date, end_date, vehicle_list):
        result = {}

        min_active_time = self.vehicle_score_params['MinActiveTime']
        signal_interval = self.vehicle_score_params['SignalInterval']

        date_filter = Q("range", Date={"gte": start_date, "lte": end_date})
        dist_filter = Q("range", EstimatedDrivingTime={"gte": min_active_time})
        score_filter = Q("range", Score={"gte": 0.01})
        vehicle_filter = Q('terms', VehicleID=vehicle_list)
        query = Q("constant_score", filter=date_filter +
                  dist_filter + score_filter + vehicle_filter)

        act_veh_aggs = A("cardinality", field="VehicleID")
        act_veh_search = self.search.query(
            query).aggs.metric("activeVehicles", act_veh_aggs)
        act_veh_resp = act_veh_search.execute()
        result["activeVehicles"] = act_veh_resp["aggregations"]["activeVehicles"]["value"]

        tot_dist_aggs = A("sum", field="EstimatedDrivingDistance")
        longest_time_aggs = A("max", field="EstimatedDrivingTime")
        longest_dist_aggs = A("max", field="EstimatedDrivingDistance")
        tot_idling_aggs = A("sum", field="IdlingPoints")
        lowest_score_aggs = A("min", field="Score")
        kpi_search = self.search.query(query).aggs.metric("totalDistance", tot_dist_aggs)\
            .aggs.metric("longestRideTime", longest_time_aggs)\
            .aggs.metric("longestRideDistance", longest_dist_aggs)\
            .aggs.metric("totalIdling", tot_idling_aggs)\
            .aggs.metric("lowestScore", lowest_score_aggs)
        kpi_resp = kpi_search.execute()["aggregations"]
        result["totalDistance"] = kpi_resp["totalDistance"]["value"]
        result["longestRideTime"] = kpi_resp["longestRideTime"]["value"]
        result["longestRideDistance"] = kpi_resp["longestRideDistance"]["value"]
        result["totalIdling"] = int(
            kpi_resp["totalIdling"]["value"]) * signal_interval
        result["lowestScore"] = kpi_resp["lowestScore"]["value"]

        return result
