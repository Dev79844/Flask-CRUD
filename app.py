from flask import Flask, request
from flask import jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv('MONGO_URI'))
db = client['flask']
collection = db['user']

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/create', methods=['POST'])
def create_record():
    data = request.json
    result = collection.insert_one(data)
    return JSONEncoder().encode({'message': 'Record created successfully!', 'id': str(result.inserted_id)}), 201
    # return jsonify(result)

@app.route('/read/<id>', methods=['GET'])
def read_record(id):
    record = collection.find_one({"_id": ObjectId(id)})
    if record:
        return JSONEncoder().encode({'record':record})
    else:
        return JSONEncoder().encode({'message': 'Record not found.'}), 404
    
@app.route('/dev', methods=['GET'])
def get_record():
    output = []
    for user in collection.find():
        print(user)
        output.append(user)

    print(output)

    # return JSONEncoder().encode(output)
    return json.dumps(output, indent=2)
    
@app.route('/update/<id>', methods=['PUT'])
def update_record(id):
    data = request.json
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.modified_count > 0:
        return JSONEncoder().encode({'message': 'Record updated successfully!'})
    else:
        return JSONEncoder().encode({'message': 'Record not found.'}), 404

@app.route('/delete/<id>', methods=['DELETE'])
def delete_record(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return JSONEncoder().encode({'message': 'Record deleted successfully!'})
    else:
        return JSONEncoder().encode({'message': 'Record not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
