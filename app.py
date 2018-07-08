from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

from bson import json_util
import json


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'TT_relevanC'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/TT_relevanC'

mongo = PyMongo(app)


@app.route('/schema/<nom_schema>', methods=['POST'])
def add_schema(nom_schema):
    collection = mongo.db.bibou
    schema_id = collection.insert(request.json)
    new_schema = collection.find_one({'_id': schema_id})
    return "ok"


@app.route('/star', methods=['GET'])
def get_all_stars():
    star = mongo.db.stars
    output = []
    for s in star.find():
        output.append({'name': s['name'], 'distance': s['distance']})
    return jsonify({'result': output})


@app.route('/star/<string:name>', methods=['GET'])
def get_one_star(name):
    star = mongo.db.stars
    print(name)
    s = star.find_one({'name': name})
    if s:
        output = {'name': s['name'], 'distance': s['distance']}
    else:
        output = "No such name"
    return jsonify({'result': output})


@app.route('/star', methods=['POST'])
def add_star():
    star = mongo.db.stars
    name = request.json['name']
    distance = request.json['distance']
    star_id = star.insert({'name': name, 'distance': distance})
    new_star = star.find_one({'_id': star_id})
    output = {'name': new_star['name'], 'distance': new_star['distance']}
    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True)
