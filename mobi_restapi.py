#!/usr/bin/python

from functools import wraps
from flask import Flask, request, Response, jsonify
from flask_restful import Resource, Api
from json import dumps
from flask_pymongo import PyMongo
from pymongo import MongoClient
import crawler


@app.route('/fahrplaene/abfahrten', methods=['POST'])
def get_testing():
    json = request.json
    output = {}
    if "station" in json.keys() and "on" in json.keys() and "at" in json.keys():
        return jsonify(crawler.request_station_info(json["station"],
                                                    json["at"],
                                                    json["on"]))
    else:
        return jsonify({"error": "data object must contain 'station', 'on', and 'start'."})


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    app.run(host='0.0.0.0', port='6425')
