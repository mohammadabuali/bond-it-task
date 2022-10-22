from flask import Flask, request, jsonify, make_response
from flights_info import FlightsInfo
import json
app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_flight_info():
    flight_info = FlightsInfo("data.csv")
    flight_requested = request.args.get('flight', default="", type=str)
    for flight in flight_info.get_flights_from_csv_file():
        if flight_requested == flight[0]:
            return jsonify(
                flight_id=flight[0],
                Departure=flight[1],
                Arrival=flight[2],
                Success=flight[3]
            )
    return make_response(json.dumps({'message': "No flight with that ID found"}), 400)

'''
Assuming That we receive in the body of the request in the format of
{"flights":[{"flight_id":{}, "departure":{}, "arrival":{}}]}
'''
@app.route('/', methods=['POST'])
def post_flights():
    data = request.get_json()
    if data.get("flights", default="", type=str):
        all_flights_to_be_updated = set()
        flight_info = FlightsInfo("data.csv")
        flights = data["flights"]
        for flight in flights:
            if "flight_id" in flights and "departure" in flights and "arrival" in flights:
                flight_info.update_flights(flight["flight_id"], flight["departure"], flight["arrival"])
                all_flights_to_be_updated.add(flight["flight_id"])
        flight_info.update_flights_file()
        if len(all_flights_to_be_updated) != 0:
            return make_response(json.dumps({'message': f'updated flights: {all_flights_to_be_updated}'}), 201)

    return make_response(json.dumps({'message': "request should be in the format of:\n {'flights':[{'flight_id':{}, 'departure':{}, 'arrival':{}}]}"}), 400)
