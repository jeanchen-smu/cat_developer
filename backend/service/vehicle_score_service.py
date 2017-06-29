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
        filters = date_filter + dist_filter + score_filter
        if len(vehicle_list)>0:
            vehicle_filter = Q('terms', VehicleID=vehicle_list)
            filters += vehicle_filter
        query = Q("constant_score", filter=filters)

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

    def get_stats(self, start_date, end_date, vehicle_list):
        stats_dict = {}

        score_dist_list = []
        avg_dist_list = []
        avg_score_list = []

        min_active_time = self.vehicle_score_params['MinActiveTime']

        date_filter = Q("range", Date={"gte": start_date, "lte": end_date})
        dist_filter = Q("range", EstimatedDrivingTime={"gte": min_active_time})
        score_filter = Q("range", Score={"gte": 0.01})
        filters = date_filter + dist_filter + score_filter
        if len(vehicle_list)>0:
            vehicle_filter = Q('terms', VehicleID=vehicle_list)
            filters += vehicle_filter
        query = Q("constant_score", filter=filters)

        date_aggs = A("date_histogram", field="Date", interval="day")
        avg_score_aggs = A("avg", field="Score")
        avg_distance_aggs = A("avg", field="EstimatedDrivingDistance")
        avg_search = self.search.query(query).extra(
            size=0).aggs.metric("average_data", date_aggs)
        avg_search.aggs["average_data"].metric("average_score", avg_score_aggs)
        avg_search.aggs["average_data"].metric(
            "average_distance", avg_distance_aggs)
        for average_data in avg_search.execute()["aggregations"]["average_data"]["buckets"]:
            date = str(average_data["key_as_string"][:10])
            avg_dist_list.append({"name": date, "value": round(
                average_data["average_distance"]["value"], 2)})
            avg_score_list.append({"name": date, "value": round(
                average_data["average_score"]["value"], 2)})

        score_dist_aggs = A("histogram", field="Score", interval=0.01)
        score_dist_search = self.search.query(query).extra(
            size=0).aggs.metric("scoreDistribution", score_dist_aggs)
        for score_dist in score_dist_search.execute()["aggregations"]["scoreDistribution"]["buckets"]:
            score_dist_list.append(
                {"name": int(score_dist["key"] * 100), "value": score_dist["doc_count"]})

        stats_dict["scoreDistribution"] = score_dist_list
        stats_dict["averageScore"] = avg_score_list
        stats_dict["averageDistance"] = avg_dist_list

        return stats_dict
