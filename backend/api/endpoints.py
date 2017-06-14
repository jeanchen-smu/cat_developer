from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required,\
    create_access_token, get_jwt_identity

app = Flask(__name__)
app.secret_key = "JWT SECRET"

jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username != 'goldbell' and password != '1234':
        return jsonify(msg="Bad username or password"), 401
    token = create_access_token(username)
    return jsonify(access_token=token), 200

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
    data = [
        ['30261', '35444', '103.90197', '1.33296', '4', '11:23:30', 0], 
        ['30608', '35442', '103.67601', '1.32753', '1', '10:10:31', 0], 
        ['30585', '35441', '103.77096', '1.38375', '1', '11:18:04', 0]
    ]
    return jsonify(data)

@app.route('/historical', methods=['GET', 'POST'])
def get_past_journeys():
    data = [
            ["35444", [
              [1.38368, 103.73796, '72', '00:00:13'], 
              [1.38963, 103.74646, '73', '00:01:13'], 
              [1.38885, 103.75676999999999, '68', '00:02:13'], 
              [1.39067, 103.76655, '66', '00:03:13'], 
              [1.39314, 103.77389000000001, '65', '00:04:13'], 
              [1.40341, 103.77308000000001, '70', '00:05:13'], 
              [1.41382, 103.77129000000001, '68', '00:06:13'], 
              [1.42139, 103.77109, '66', '00:07:13'], 
              [1.4263299999999999, 103.77999, '74', '00:08:13']
            ]]
          ]
    return jsonify(data)		