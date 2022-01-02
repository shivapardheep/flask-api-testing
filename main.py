import json

from flask_pymongo import *
from flask import *

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://apitest:Shiva12345@cluster0.q8a2d.mongodb.net/first_db?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db.students
app.secret_key = 'abc'

@app.route('/',methods=['GET','POST'])
def home():
    try:
        res = db.find()
        lis = [x for x in res]
        return jsonify(lis)
    except:
        return jsonify({"Result": "Error Accu   red...."})

@app.route('/viewall/',methods=['GET','POST'])
def viewall():
    try:
        res = db.find()
        return jsonify([x for x in res])
    except:
        return {"Result":"Error Accured...."}

@app.route('/view/<int:userid>',methods=['GET','POST'])
def view(userid):
    res = db.find_one({"_id":userid})
    return jsonify(res)

@app.route('/insert/',methods=['GET','POST'])
def insert():
    if request.method == 'POST':
            data = request.data
            data = data.decode()
            data = json.loads(data)
            regno = data['regno']
            name = data['name']
            age = data['age']
            email = data['email']
            find = db.find_one({"_id":int(regno)})
            if(str(find)=='None'):
                try:
                    res = db.insert_one({'_id': regno, 'name': name, 'age': age, 'email': email})
                    scs = {"Result": "Successfully Created..."}
                    return scs
                except:
                    return {"Result":"error"}
            else:
                return {"Result":"duplicate entry..."}

#update
@app.route('/update/',methods=['PUT'])
def Update():
    if request.method == 'PUT':
        try:
            data = request.data
            data = data.decode()
            data = json.loads(data)
            regno = data['regno']
            name = data['name']
            age = data['age']
            email = data['email']
            update = {"$set": {"name": name,'age':age,"email": email}}
            where = {"_id": regno}
            db.update_many(where, update)
            return {"Result": "Data Updated Successfully..."}
        except:
            return {"Result": "Something went wrong..."}

@app.route('/delete/<int:userid>/',methods=['DELETE'])
def delete(userid):
    if request.method == 'DELETE':
        try:
            db.delete_one({"_id":userid})
            return {"Result": "Data Deleted Sucessfully..."}
        except:
            return {"Result": "Something went wrong Error Accured..."}

if __name__ == "__main__":
    app.run(debug=True)
