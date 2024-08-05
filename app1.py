from flask import Flask,request,jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app1 = Flask(__name__)

client=MongoClient("mongodb://localhost:27017")
db = client["product"]
collection=db["item"]
@app1.route("/addproduct" , methods=['POST'])
def addproduct():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'_id':str(result.inserted_id)})

@app1.route("/getproduct" , methods=['GET'])
def getproduct():
    result = list(collection.find()) 
    for results in result:
        results['_id'] = str(results['_id'])
    return jsonify(result)


@app1.route("/putproduct/<_id>", methods=['PUT'])
def putproduct(_id):
    data = request.json
    object_id = ObjectId(_id)
    result = collection.update_one({'_id': object_id}, {'$set': data})
    return jsonify({"MESSAGE": "PRODUCT UPDATED"})
#    return jsonify({'_id':str(result)})


@app1.route("/deleteproduct/<_id>", methods=['DELETE'])
def deleteproduct(_id):
    data = request.json
    object_id =ObjectId(_id)
    result = collection.delete_one({'_id': object_id})
    return jsonify({"MESSAGE": "PRODUCT DELETED"})

@app1.route("/getsproduct/<_id>", methods=['GET'])
def getsproduct(_id):
    object_id=ObjectId(_id)
    result=collection.find_one({'_id':object_id})
    result['_id'] = str(result['_id'])
    return jsonify(result)
    


if __name__=="__main__":
    app1.run(debug=True)