from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required,\
    create_access_token, get_jwt_identity
from service.vehicle_service import VehicleService
from service.position_service import PositionService

app = Flask(__name__)
app.secret_key = "JWT SECRET"

jwt = JWTManager(app)

vs = VehicleService()
ps = PositionService()

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'goldbell' and password == '1234':
        token = create_access_token(username)
        return jsonify(access_token=token, msg="Success"), 200
    
    return jsonify(access_token="", msg="Bad username or password"), 401
    
@app.route("/rank", methods=["GET"])
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
    data = [
        {"Rank": 1, "Vehicle ID": "36391", "Kind": "truck", "Score": 0.99, "Max Overspeed": 5, "Driving Time": 6.59, "Distance": 246.5},
        {"Rank": 2, "Vehicle ID": "35281", "Kind": "truck", "Score": 0.89, "Max Overspeed": 10, "Driving Time": 5.50, "Distance": 246.5},
        {"Rank": 3, "Vehicle ID": "26393", "Kind": "van", "Score": 0.89, "Max Overspeed": 10, "Driving Time": 8.95, "Distance": 346.5},
        {"Rank": 4, "Vehicle ID": "56391", "Kind": "truck", "Score": 0.79, "Max Overspeed": 15, "Driving Time": 7.50, "Distance": 296.5},
        {"Rank": 5, "Vehicle ID": "66917", "Kind": "van", "Score": 0.75, "Max Overspeed": 17, "Driving Time": 2.45, "Distance": 46.5},
        {"Rank": 6, "Vehicle ID": "36312", "Kind": "truck", "Score": 0.73, "Max Overspeed": 18, "Driving Time": 3.95, "Distance": 146.5},
    ]
    
    return jsonify(data)

@app.route('/realtime', methods=['GET', 'POST'])
def get_realtime_location():
    #vehicleList = request.args.get('vehicleList')
    vehicle_list = [29696, 29705, 29704, 35114, 34758, 34966]

    data = vs.select_latest_position(vehicle_list)
    return jsonify(data)

@app.route('/historical', methods=['GET', 'POST'])
def get_past_journeys():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    date = start_date
    #vehicleList = requeste.args.get('vehicleList')
    vehicle_list = [34758, 35114, 29705, 29696, 29704, 34966]

    data = []
    for vehicle in vehicle_list: 
        data.append([str(vehicle), ps.select_vehicle_position(date,vehicle)])

    return jsonify(data)	

@app.route('/overview', methods=['GET', 'POST'])
def get_overview_coordinates(): 
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    date = end_date
    #vehicle_list = request.args.get('vehicleList')
    vehicle_list = [29705, 29696, 29704, 34758, 35114, 34966]
    raw_position_data = ps.select_all_position(date, vehicle_list)
    data = []
    for position in raw_position_data:
        position = [str(position['Lat']), str(position['Lon']), str(position['Speed']), str(position['VehicleID'])]
        data.append(position)
    return jsonify(data)	