import pdb

from flask import Flask, jsonify, request
from flask_cors import CORS
from autoria_grabber import AutoriaGrabber
from bidfax_grabber import BidfaxGrabber
import json

app = Flask(__name__)
CORS(app)

autoria_grabber = AutoriaGrabber()
bidfax_grabber = BidfaxGrabber()

@app.route('/autoria', methods=['POST'])
def autoria_post():
    data = request.json
    res = autoria_grabber.grab(data['url'])

    # Convert array of named tuples to list of dictionaries
    res_dicts = [r._asdict() for r in res]

    # Convert list of dictionaries to JSON
    json_data = json.dumps({'cars': res_dicts})

    return json_data
@app.route('/bidfax/<vin>', methods=['GET'])
def bidfax_get(vin):
    res = bidfax_grabber.grab(vin)
    return jsonify({'result': res})


if __name__ == '__main__':
    app.run(debug=True)

