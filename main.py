"""Main Entrypoint for the Application"""

import logging
import json
import base64

from flask import Flask, request
from flask import jsonify
import utility

from capital import Capital

app = Flask(__name__)


@app.route('/')
def hello_world():
    """hello world"""
    return 'Hello World!'

@app.route('/api/status', methods=['GET'])
def get_status():
    status = dict()
    status['insert'] = True
    status['fetch'] = True
    status['delete'] = True
    status['list'] = True
    return json.dumps(status), 200


@app.route('/api/capitals/<id>', methods=['DELETE'])
def delete(id):
    if not id:
        server_error('Unexpected error')
        return

    capital = Capital()
    try:
        capital.delete(id)
        return "Capital object delete status", 200
    except Exception as ex:
        return not_found_error('Capital record not found')

@app.route('/api/capitals/<id>', methods=['GET'])
def get(id):
    if not id:
        server_error('Unexpected error')
        return

    capital = Capital()
    try:
        output = capital.get(id)
        return json.dumps(output), 200
    except Exception as ex:
        return not_found_error('Capital not found')

@app.route('/api/capitals/<id>', methods=['PUT'])
def insert(id):
    if not id:
        return server_error('Unexpected error')

    capital = Capital()
    input = request.get_json()
    capital.insert(id, input)
    return 'Successfully stored the capital', 200

@app.route('/api/capitals', methods=['GET'])
def get_all():
    capital = Capital()
    try:
        output = capital.get_all()
        return json.dumps(output), 200
    except Exception as ex:
        return not_found_error('Capital not found')

@app.errorhandler(404)
def not_found_error(err):
    """Error handler"""
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 404

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
