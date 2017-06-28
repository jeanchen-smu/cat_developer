from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required,\
    create_access_token, get_jwt_identity
from service.vehicle_service import VehicleService
from service.position_service import PositionService
from service.vehicle_score_service import VehicleScoreService
import pdb

app = Flask(__name__)
app.secret_key = "JWT SECRET"

jwt = JWTManager(app)

vehicle_service = VehicleService()
position_service = PositionService()
vehicle_score_service = VehicleScoreService()


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'goldbell' and password == '1234':
        token = create_access_token(username)
        return jsonify(access_token=token, msg="Success"), 200

    return jsonify(access_token="", msg="Bad username or password"), 401


@app.route("/rank", methods=["GET", 'POST'])
@jwt_required
def get_vehicle_ranks():
    header_fields = [
        "Rank",
        "Vehicle ID",
        "Kind",
        "Score",
        "Max Overspeed",
        "Driving Time",
        "Distance"
    ]

    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    vehicle_list = request.args.get('vehicleList')

    #c = 1/0

    print(start_date)
    if vehicle_list is None:
        vehicle_list = vehicle_service.get_all_vehicles()

    raw_score_data = vehicle_score_service.select_score_by_date_range(
        start_date, end_date, vehicle_list)
    sorted_score_data = sorted(
        raw_score_data, key=lambda x: x['Score'], reverse=True)

    data = []
    for score in sorted_score_data:
        data.append({"Rank": sorted_score_data.index(score) + 1,
                     "Vehicle ID": str(score['VehicleID']),
                     "Kind": "truck",
                     "Score": score['Score'],
                     "Max Overspeed": score['MaxSpeed'],
                     "Driving Time": score['EstimatedDrivingTime'],
                     "Distance": score['EstimatedDrivingDistance']})

    return jsonify(data)


@app.route('/realtime', methods=['GET', 'POST'])
def get_realtime_location():
    vehicle_list = request.args.get('vehicleList')

    if vehicle_list is None:
        vehicle_list = vehicle_service.get_all_vehicles()

    data = vehicle_service.select_latest_position(vehicle_list)
    return jsonify(data)


@app.route('/historical', methods=['GET', 'POST'])
def get_past_journeys():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
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
    data = {
        'activeVehicles': 100,
        'totalDistance': 1000,
        'longestRideTime': 2,
        'longestRideDistance': 150,
        'totalIdling': 10,
        'lowestScore': 0
    }
    return jsonify(data)


@app.route('/stats', methods=['POST'])
def get_stats():
    data = {
        'scoreDistribution': [
            {'name': 'Jan', 'value': 3700},
            {'name': 'Feb', 'value': 3700},
            {'name': 'Mar', 'value': 3700},
            {'name': 'Apr', 'value': 3700},
            {'name': 'May', 'value': 3700},
            {'name': 'Jun', 'value': 3700},
            {'name': 'Jul', 'value': 3700},
            {'name': 'Aug', 'value': 3700},
            {'name': 'Sep', 'value': 3700},
            {'name': 'Oct', 'value': 3700},
            {'name': 'Nov', 'value': 3700},
            {'name': 'Dec', 'value': 3700}
        ],
        averageScore: [
            {'name': 'Nov', 'value': 3700},
            {'name': 'Nov', 'value': 3700},
            {'name': 'Nov', 'value': 3700},
            {'name': 'Nov', 'value': 3700},
            {'name': 'Nov', 'value': 3700},
            {'name': 'Nov', 'value': 3700},
            {'name': 'Nov', 'value': 3700}
        ],
        averageDistance: [
            {'name': 'Nov', 'value': 2400},
            {'name': 'Nov', 'value': 1398},
            {'name': 'Nov', 'value': 9800},
            {'name': 'Nov', 'value': 3908},
            {'name': 'Nov', 'value': 4800},
            {'name': 'Nov', 'value': 3490},
            {'name': 'Nov', 'value': 4300},
            {'name': 'Nov', 'value': 4300},
            {'name': 'Nov', 'value': 4300},
            {'name': 'Nov', 'value': 4300},
            {'name': 'Nov', 'value': 4300}
        ]
    }
    return jsonify(data)


@app.route('/overview', methods=['GET', 'POST'])
def get_overview_coordinates():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    vehicle_list = request.args.get('vehicleList')

    if vehicle_list is None:
        vehicle_list = vehicle_service.get_all_vehicles()

    raw_position_data = position_service.select_all_position(
        end_date, vehicle_list)
    data = []
    for position in raw_position_data:
        position = [str(position['Lat']), str(position['Lon']), str(
            position['Speed']), str(position['VehicleID'])]
        data.append(position)
    return jsonify(data)
