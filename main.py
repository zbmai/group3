"""Main Entrypoint for the Application"""

import json
import logging
import urlparse
from google.cloud import pubsub
from flask import Flask, request, jsonify, render_template
from capital import Capital
from cloudstorage import Storage
import utility

app = Flask(__name__)
capital = Capital()
storage = Storage()
client = pubsub.Client()


@app.route('/', methods=['GET'])
@app.route('/map', methods=['GET'])
def show_map():
    results = capital.get_all()
    return render_template('map.html', comment=None, results=results)

@app.route('/polymer', methods=['GET'])
def show_polymer_map():
    results = capital.get_all()
    return render_template('polymer_maps.html', comment=None, results=results)

@app.route('/countries', methods=['GET'])
def list_countries():
    results = capital.get_all_countries()
    return render_template('countries.html', comment=None, results=results)

@app.route('/api/status', methods=['GET'])
def get_status():
    status = dict()
    status['insert'] = True
    status['fetch'] = True
    status['delete'] = True
    status['list'] = True
    status['query'] = True
    status['search'] = True
    status['pubsub'] = True
    status['storage'] = True
    return jsonify(status), 200

@app.route('/api/capitals/<int:id>', methods=['DELETE'])
def delete(id):
    if not id:
        server_error('Unexpected error')
        return

    try:
        capital.delete(id)
        return ok_message("Capital object delete status")
    except Exception as ex:
        return not_found_error('Capital record not found')

@app.route('/api/capitals/<int:id>', methods=['GET'])
def get(id):
    if not id:
        server_error('Unexpected error')
        return
    try:
        output = capital.get(id)
        return jsonify(output), 200
    except Exception as ex:
        return not_found_error('Capital not found')

@app.route('/api/capitals/<int:id>', methods=['PUT'])
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
    query = par.get('query', None)
    search = par.get('search', None)
    try:
        if query:
            first = query[0]
            pair = first.split(':')
            key = pair[0]
            value = pair[1]
            output = capital.query(key, value)
        elif search:
            value = search[0]
            output = capital.search(value)
        else:
            output = capital.get_all_max20()
        return jsonify(output), 200
    except Exception as ex:
        return not_found_error('Capital not found')

@app.route('/api/capitals/<int:id>/publish', methods=['POST'])
def publish(id):
   if not id:
       return server_error('Unexpected error')

   try:
       entity = capital.get(id)
   except Exception:
       return not_found_error('Capital record not found')

   try:
       input = request.get_json()
       part = input['topic'].split('/')
       topicName = part[-1]
       if len(part) > 1:
           projectName = part[1]
       else:
           projectName = 'hackathon-team-003'
       utility.log_info(topicName)
       client = pubsub.Client(project=projectName)
       topic = client.topic(topicName)
       if topic.exists():
           text = json.dumps(entity)
           encoded = text.encode('utf-8')
           messageid = topic.publish(encoded)
           res = {}
           res['messageId'] = int(messageid)
           return jsonify(res), 200
       else:
           return not_found_error('Topic does not exist')
   except Exception as ex:
       return server_error('Unexpected error')

@app.route('/api/capitals/<int:id>/store', methods=['POST'])
def store(id):
    if not id:
        return server_error('Unexpected error')

    try:
        entity = capital.get(id)
    except Exception:
        return not_found_error('Capital record not found')

    try:
        input = request.get_json()
        bucketName = input['bucket']
        if not storage.check_bucket(bucketName):
            ok = storage.create_bucket(bucketName)
            if not ok:
                return server_error('Unexpected error')

        if storage.store_file_to_gcs(bucketName,id, entity):
            return ok_message('Successfully stored in GCS')
        else:
            return not_found_error('Capital records not found')
    except Exception as ex:
        return server_error('Unexpected error')

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
