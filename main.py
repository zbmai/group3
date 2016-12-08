"""Main Entrypoint for the Application"""

import json
import logging
import urlparse
from google.cloud import pubsub

from flask import Flask, request, jsonify

from capital import Capital

app = Flask(__name__)
capital = Capital()

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
    status['query'] = True
    status['search'] = False
    status['pubsub'] = False
    status['storage'] = False
    return jsonify(status), 200


@app.route('/api/capitals/<id>', methods=['DELETE'])
def delete(id):
    if not id:
        server_error('Unexpected error')
        return

    try:
        capital.delete(id)
        return ok_message("Capital object delete status")
    except Exception as ex:
        return not_found_error('Capital record not found')

@app.route('/api/capitals/<id>', methods=['GET'])
def get(id):
    if not id:
        server_error('Unexpected error')
        return

    try:
        output = capital.get(id)
        return jsonify(output), 200
    except Exception as ex:
        return not_found_error('Capital not found')

@app.route('/api/capitals/<id>', methods=['PUT'])
def insert(id):
    if not id:
        return server_error('Unexpected error')

    try:
        input = request.get_json()
        capital.insert(id, input)
        return ok_message('Successfully stored the capital')
    except Exception as ex:
        return server_error('Unexpected error')

@app.route('/api/capitals', methods=['GET'])
def query():
    url = request.url
    par = urlparse.parse_qs(urlparse.urlparse(url).query)
    values = par.get('query', None)
    if values:
        value = values[0]
        pair = value.split(':')
        try:
            output = capital.query(pair[0], pair[1])
            return jsonify(output), 200
        except Exception as ex:
            return not_found_error('Capital not found')
    else:
        return get_all()

def get_all():
    try:
        output = capital.get_all()
        return jsonify(output), 200
    except Exception as ex:
        return not_found_error('Capital not found')

@app.route('/api/capitals/{id}/publish', methods=['POST'])
def publish(id):
    print id


def ok_message(msg):
    okMessage = {}
    okMessage['code'] = 200
    okMessage['message'] = msg
    return jsonify(okMessage), 200

@app.errorhandler(404)
def not_found_error(err):
    """Error handler"""
    logging.exception('An error occurred during a request - {}'.format(err))
    errorMessage={}
    errorMessage['code'] = 404
    errorMessage['message'] = err
    return jsonify(errorMessage), 404

@app.errorhandler(500)
def server_error(err):
    """Error handler"""
    logging.exception('An error occurred during a request - {}'.format(err))
    errorMessage = {}
    errorMessage['code'] = 500
    errorMessage['message'] = err
    return jsonify(errorMessage), 500


if __name__ == '__main__':
    # Used for running locally
    app.run(host='127.0.0.1', port=8080, debug=True)
