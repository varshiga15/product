from flask import Flask,request,jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import re

user = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client["user"]
collection = db["details"]

@user.route("/adduser", methods = ['POST'])
def adduser():
    data = request.json
    email=data.get("email")
    
    if collection.find_one({"email": email}):
        return ("error! email already exist")
    
    if data:
        result = collection.insert_one(data)
        return jsonify({'_id':str(result.inserted_id)})
    else:
        return jsonify({"error invalid data"})
    
@user.route("/getlogin", methods = ['GET'])
def getlogin():
    user = request.json
    name = user.get("username")

    if collection.find_one({"username":name}):
        return("login success")
    if user:
        result = collection.find_one(user)
        return jsonify({'_id':str(result)})
    else:
        return jsonify({"error invaild data"})
    
@user.route('/detail', methods = ['POST'])
def detail():
    data = request.json
    email = data.get("email")
    mobile = data.get("phone no")
    password =data.get("password")

    email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    if not re.match(email_regex,email):
        return jsonify({"error":"email is invaild"})
    
    phone_regex = r'^\d{10}$'

    if not re.match(phone_regex,mobile):
        return jsonify({"error":"phone no is invaild"})
    
    if len(password)<8:
        return jsonify({"error":"password must be at least 8 characters long"})
    if not re.search(r"[A-Z]", password):
        return jsonify({"error":"password must contain at least one upper case"})
    if not re.search(r"[a-z]", password):
        return jsonify({"error":"password must contain at least one lower case"})
    if not re.search(r"\d", password):
        return jsonify({"error":"password must contain at least one digit"})
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
         return jsonify({"error":"password must contain at least one special characters"})
    
    
    
    if collection.find_one({"email": email}):
        return jsonify({"message": "Email is already registered"})
    
    if collection.find_one({"phone no": mobile}):
        return jsonify({"message": "Phone number is already registered"})
    




    if data:
        result = collection.insert_one(data)
        return jsonify({"_id":str(result.inserted_id)})
    else:
        return jsonify({"error invald data"})
    


if __name__ == ("__main__"):
    user.run(debug=True)
