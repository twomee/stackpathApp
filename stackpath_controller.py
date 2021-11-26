import json

from flask import Flask, request

from properties_object_module import properties_object
from stackpath_service_module import stackpath_service_module

config = properties_object()
config.load_properties()
app = Flask(__name__)
service = stackpath_service_module(config)


@app.route('/add', methods=['POST'])
def add_domains():
    try:
        content = request.get_json()
        timestamp = content.get("timestamp")
        service.add_domain_requests(timestamp, content)
        return json.dumps({'status': "success"}, default=list), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'status': "fail ==>" + f" {e}"}), 404, {'ContentType': 'application/json'}


@app.route('/get_stat', methods=['GET'])
def get_stat():
    try:
        content = request.get_json()
        type = content.get("type")
        domain_stats = service.get_stats(type)

        return json.dumps({'result': domain_stats}, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'result': "fail ==>" + f" {e}"}), 404, {'ContentType': 'application/json'}


@app.route('/clear_all', methods=['GET'])
def clear_all():
    try:
        service.delete_all_data()
        return json.dumps({'result': "success"}, default=str), 200, {'ContentType': 'application/json'}
    except Exception as e:
        return json.dumps({'result': "fail ==>" + f" {e}"}), 404, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
