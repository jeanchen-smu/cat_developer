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

@app.route('/realtime', methods=['POST'])
def get_realtime_location():
    vehicle_list = request.args.get('vehicleList')

    data=[]
    for veh in baseride.get_vehicle( 'e62a48f233'):
        if vehicle_list and veh['id'] not in vehicle_list:
            continue
        rec = {
            'VehicleID': veh['id'],
            'Lat': veh['position']['lat'],
            'Lon': veh['position']['lon'],
            'Speed': veh['position']['speed'],
            'DeviceTS': veh['position']['device_ts']
        }
        data.append(rec)

    return jsonify(data)


@app.route('/historical', methods=['GET', 'POST'])
def get_past_journeys():
    start_date = to_date(request.args.get('startDate'))
    end_date = to_date(request.args.get('endDate'))
    vehicle_list = request.args.get('vehicleList')

    if vehicle_list is None:
        vehicle_list = vehicle_service.get_all_vehicles()

    data = []
    for vehicle in vehicle_list:
        data.append(
            [str(vehicle), position_service.select_vehicle_position(end_date, vehicle)])

    return jsonify(data)


@app.route('/kpi', methods=['POST'])
def get_kpi():
    start_date = to_date(request.json.get('startDate'))
    end_date = to_date(request.json.get('endDate'))
    vehicle_list = request.json.get('vehicleList')
    data = vehicle_score_service.get_kpis(start_date, end_date, vehicle_list)
    return jsonify(data)


@app.route('/stats', methods=['POST'])
def get_stats():
    start_date = to_date(request.json.get('startDate'))
    end_date = to_date(request.json.get('endDate'))
    vehicle_list = request.json.get('vehicleList')
    # pdb.set_trace()
    data = vehicle_score_service.get_stats(start_date, end_date, vehicle_list)
    return jsonify(data)


@app.route('/overview', methods=['POST'])
def overview():
    filter = {
        'start_date': to_date(request.json.get('startDate')),
        'end_date': to_date(request.json.get('endDate')),
        'vehicle_list': request.json.get('vehicleList')
        }
    
    data = []
    #pdb.set_trace()
    position_service.vehicle_position(filter, data)
    return jsonify(data)

