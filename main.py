"""Main Entrypoint for the Application"""

import logging
import json
import base64

from flask import Flask, request
from flask import jsonify
import utility


app = Flask(__name__)


@app.route('/')
def hello_world():
    """hello world"""
    return 'Hello World!'

@app.route('/api/status', methods=['GET'])
def get_status():
    status = dict()
    status['insert'] = False
    status['fetch'] = False
    status['delete'] = False
    status['list'] = False
    return json.dumps(status), 200


@app.route('/api/capitals/<id>', methods=['DELETE'])
def delete(id):
    return 'Not done yet', 400

@app.route('/api/capitals/<id>', methods=['GET'])
def get(id):
    return 'Not done yet', 400

@app.route('/api/capitals/<id>', methods=['PUT'])
def insert(id):
    return 'Not done yet', 400

@app.route('/api/capitals', methods=['GET'])
def get_all():
    return 'Not done yet', 400

@app.errorhandler(500)
def server_error(err):
    """Error handler"""
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500


if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)
