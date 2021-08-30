from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from datetime import timedelta
from helper_functions import (
    add_template,
    fetch_template,
    remove_template,
    update_template,
)

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

jwt = JWTManager(app)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)


@app.route("/")
def welcome_url():
    """
    Welcome endpoint
    """
    return jsonify({"message": "developed by Raviraj"})


@app.route("/register", methods=["POST"])
def register():
    """
    This endpoint will onboard new user if user hit POST request.
    User need to send first name, last name, email and password
    """
    data = request.json
    email = data["email"]
    password = data["password"]
    existing_user = mongo.db.accounts.find_one({"email": email})
    if existing_user:
        return {"message": "User already exist"}
    try:
        data["password"] = bcrypt.generate_password_hash(
            password
        )  # encrypting user password
        mongo.db.accounts.insert_one(data)
        return jsonify({"message": "user added successfully"})
    except:
        return jsonify({"message": "please try again"})


@app.route("/login", methods=["POST"])
def login():
    """
    This endpoint will take care of user authentication
    """
    email = request.json["email"]
    password = request.json["password"]
    try:
        existing_user = mongo.db.accounts.find_one({"email": email})
    except:
        return jsonify({"message": "Try after sometime"})

    if existing_user:
        if bcrypt.check_password_hash(existing_user["password"], password):
            access_token = create_access_token(
                identity=email, expires_delta=timedelta(days=1)
            )
            return jsonify(
                {"message": "Login successfully", "access_token": access_token}
            )
        else:
            return jsonify({"message": "Wrong Password"})

    else:
        return jsonify({"message": "User is not registered."})


@app.route("/template/<id>", methods=["GET", "PUT", "DELETE"])
@app.route("/template", methods=["GET", "POST"])
@jwt_required()
def template_crud(id=None):
    """
    This endpoint will work for CRUD operation
    GET:- This method will return owner owned record only.
    POST:- Will add record in database
    GET+id:- will show perticular template
    PUT+id:- update the perticular template
    DELETE+id:- delete the template
    """
    current_user = get_jwt_identity()
    data = request.json

    if request.method == "POST":
        return jsonify(add_template(mongo, data, current_user))
    elif request.method == "GET" and id == None:
        return jsonify(fetch_template(mongo, current_user))
    elif request.method == "GET" and id:
        return jsonify(fetch_template(mongo, current_user, id=id))
    elif request.method == "DELETE":
        return jsonify(remove_template(mongo, current_user, id=id))
    elif request.method == "PUT":
        return jsonify(update_template(mongo, current_user, data, id))
    else:
        return jsonify({"current_user": current_user, "id": id})


if __name__ == "__main__":
    app.run(debug=True)
