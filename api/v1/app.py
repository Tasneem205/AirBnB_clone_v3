#!/usr/bin/python3
"""
main app to run flask
"""
from flask import Flask, Response
from models import storage
from api.v1.views import app_views
import os
import json

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    data = {"error": "Not found"}
    json_data = json.dumps(data, indent=4) + '\n'
    response = Response(json_data, mimetype='application/json')
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
