from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required,\
    create_access_token, get_jwt_identity
from service.vehicle_service import VehicleService
from service.position_service import PositionService
from service.vehicle_score_service import VehicleScoreService
from utils.time_helper import TimeHelper
from provider.data_helper import Baseride
import pdb

app = Flask(__name__)
app.secret_key = "JWT SECRET"
jwt = JWTManager(app)

vehicle_service = VehicleService()
position_service = PositionService()
vehicle_score_service = VehicleScoreService()
time_helper = TimeHelper()
baseride = Baseride()
accessible_vehicles = vehicle_service.vehicle_ids()


def to_date(utc_string):
    return time_helper.convert_local_date(utc_string)


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'goldbell' and password == '1234':
        token = create_access_token(username)
        return jsonify(access_token=token, msg="Success"), 200

    return jsonify(access_token="", msg="Bad username or password"), 401


@app.route("/rank", methods=['POST'])
@jwt_required
def get_vehicle_ranks():
    start_date = to_date(request.json.get('startDate'))
    end_date = to_date(request.json.get('endDate'))

    data = vehicle_score_service.get_rank(
        start_date, end_date)

    return jsonify(data)


@app.route('/kpi', methods=['POST'])
@jwt_required
def get_kpi():
    start_date = to_date(request.json.get('startDate'))
    end_date = to_date(request.json.get('endDate'))
    vehicle_list = request.json.get('vehicleList')
    data = vehicle_score_service.get_kpis(start_date, end_date, vehicle_list)
    return jsonify(data)


@app.route('/stats', methods=['POST'])
@jwt_required
def get_stats():
    start_date = to_date(request.json.get('startDate'))
    end_date = to_date(request.json.get('endDate'))
    vehicle_list = request.json.get('vehicleList')
    # pdb.set_trace()
    data = vehicle_score_service.get_stats(start_date, end_date, vehicle_list)
    return jsonify(data)


@app.route('/overview', methods=['POST'])
@jwt_required
def overview():
    filter = {
        'start_date': to_date(request.json.get('startDate')),
        'end_date': to_date(request.json.get('endDate')),
        'vehicle_list': request.json.get('vehicleList')
    }
    data = []
    position_service.vehicle_position(filter, data)
    return jsonify(data)


@app.route('/realtime', methods=['POST'])
@jwt_required
def get_realtime_location():
    vehicle_list = request.json.get('vehicleList')
    data = []

    for veh in baseride.get_vehicle('e62a48f233'):
        if vehicle_list and veh['id'] not in vehicle_list:
            continue
        rec = {
            'VehicleID': str(veh['id']),
            'Lat': float(veh['position']['lat']),
            'Lon': float(veh['position']['lon']),
            'Speed': veh['position']['speed'],
            'DeviceTS': veh['position']['device_ts']
        }
        data.append(rec)

    return jsonify(data)


@app.route('/historical', methods=['GET', 'POST'])
@jwt_required
def get_past_journeys():
    filter = {
        'start_date': to_date(request.json.get('startDate')),
        'end_date': to_date(request.json.get('endDate')),
        'vehicle_list': request.json.get('vehicleList')
    }

    data = {}
    position_service.get_trips(filter, data)
    return jsonify(data)

@app.route('/vehicles', methods=['GET', 'POST'])
@jwt_required
def get_vehicles():
    return jsonify(accessible_vehicles)

# Retrieve the months during which a rebate is applicable
@app.route('/month', methods=['GET', 'POST'])
@jwt_required
def get_months():
    data = ["June 2017"]
    return jsonify(data)

@app.route('/monthly_discount', methods=['GET', 'POST'])
@jwt_required
def get_monthly_discount():
    month = request.json.get('month')
    if month == 'June 2017':
        data = {
            "claims": 1,
            "mileage": 2487.02,
            "score": 0.87,
            "crossSell": 1,
            "pilotProgram": 1,
            "rebate": 437.5
        }
    elif month == 'July 2017': 
        data = {
            "claims": 0,
            "mileage": 700,
            "score": 0.88,
            "crossSell": 1,
            "pilotProgram": 1,
            "rebate": 437.5
        }
    else:
        data = {
            "claims": 0,
            "mileage": 700,
            "score": 0.88,
            "crossSell": 1,
            "pilotProgram": 1,
            "rebate": 437.5
        }
    return jsonify(data)

@app.route('/score', methods=['GET', 'POST'])
@jwt_required
def get_scoring_stats():
    month = request.json.get('month')
    start_date, end_date = time_helper.convert_month(month)
    data = {}
    avg_score_list = vehicle_score_service.get_monthly_score(accessible_vehicles)
    score_dist_list = vehicle_score_service.get_score_dist(start_date, end_date, accessible_vehicles)
    data["scoreDistribution"] = score_dist_list
    data["averageScore"] = avg_score_list
    return jsonify(data)

@app.route('/mileage', methods=['GET', 'POST'])
@jwt_required
def get_mileage_stats():
    month = request.json.get('month')
    start_date, end_date = time_helper.convert_month(month)
    data = {}
    avg_distance_list = vehicle_score_service.get_monthly_mileage(accessible_vehicles)
    distance_dist_list = []
    data["distanceDistribution"] = distance_dist_list
    data["averageDistance"] = avg_distance_list
    return jsonify(data)

@app.route('/accident', methods=['GET', 'POST'])
@jwt_required
def get_accidents():
    filter = {
        'start_date': to_date(request.json.get('startDate')),
        'end_date': to_date(request.json.get('endDate')),
        'vehicle_list': request.json.get('vehicleList')
    }
    data = {}
    coordinates = {}

    vehicle = filter['vehicle_list'][0]
    position_service.get_trips(filter, coordinates)
    data["coordinates"] = coordinates.get(vehicle)
    data["events"] = {
        "Harsh Braking": [
            {
                "Lat": 1.371912490015,
                "Long": 103.89906305231,
                "DeviceTS": "2017-07-19 15:59:54",
                "Speed": 1 
            }
        ],
        "Harsh Acceleration": []
    }
    return jsonify(data)