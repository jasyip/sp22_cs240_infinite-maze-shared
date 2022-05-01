# PROOF-OF-CONCEPT FOR MULTIPLE MAZE SEGMENTS
# This MG returns an empty segment for (0,0), and the given static maze from week 1 for the 8 surrounding maze tiles.

import json
import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

MG_NAME = 'blotch'

# load config file
with open('../config.json', 'r') as f:
    config = json.load(f)
MAIN_URL = config['main_url']
MAIN_PORT = config['main_port']

app = Flask(__name__)

# add self to middleware
load_dotenv()
port = int(os.getenv('FLASK_RUN_PORT'))
data = {'name': MG_NAME, 'url': f'{MAIN_URL}:{port}', 'author': config['author']}
if 'RNG_WEIGHT' in os.environ:
    weight = float(os.getenv('RNG_WEIGHT'))
    data['weight'] = weight
requests.put(f'{MAIN_URL}:{MAIN_PORT}/addMG', data=json.dumps(data), headers={'Content-Type': 'application/json'})


given_segment = ["9aa2aac", "59aaaa4", "51aa8c5", "459a651", "553ac55", "559a655", "3638a26"]
blank_segment = ['988088c', '1000004', '1000004', '0000000', '1000004', '1000004', '3220226']


@app.route('/generate', methods=['GET'])
def generate():
    print('==Incoming JSON==')
    print(request.json)

    output = {}
    output['geom'] = blank_segment

    row = 0
    col = 0
    if 'row' in request.args.keys():
        row = int(request.args['row'])
    if 'col' in request.args.keys():
        col = int(request.args['col'])

    # load given_segment into 8 surrounding tiles
    output['extern'] = {}
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            output['extern'][f'{r}_{c}'] = {'geom': given_segment}

    print('==Outgoing JSON==')
    print(output)
    return jsonify(output), 200
