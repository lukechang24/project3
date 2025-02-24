import models

from flask import request, jsonify, Blueprint, redirect 
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user')
# user = Blueprint("users", "user", url_prefix="/user")

###############this is the controller basically
@user.route('/', methods=["GET"])
def test():
    return 'for surely'

@user.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['username'] = payload['username'].lower()
    payload['email'] = payload['email'].lower()
    print(payload)
    try:
        models.User.get(models.User.email == payload['email']) 
        return jsonify(data={}, status={"code": 401, "message": "Username/Email already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password']) 
        user = models.User.create(**payload) 
        login_user(user) 
        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        del user_dict['password']
        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload, '< --- this is playload')
    try:
        user = models.User.get(models.User.username == payload['username'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print(user, ' this is user')
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})


@user.route('/logout')
def logout():
    print("hitting here clicked button")
    logout_user()
    return jsonify(data={}, status={"code": 202, "message": "logged out success"})
