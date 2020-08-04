from flask import Blueprint, request, jsonify
from flask_login import login_user,logout_user,current_user,UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
auth = Blueprint('auth', __name__)

@auth.route('/api/v1/register', methods=['POST'])
def register_post():
    register_creds = request.get_json()
    username = register_creds['username']
    password = generate_password_hash(register_creds['password'])
    UserObj = User.query.filter_by(username=username).first()
    if UserObj:
        return jsonify(msg='user already exists'), 200
    new_User = User(username=username, password=password)
    db.session.add(new_User)
    db.session.commit()
    return jsonify(msg='user added successfully !'), 200

@auth.route('/api/v1/login', methods=['POST'])
def login_post():
    login_creds = request.get_json()
    username = login_creds['username']
    UserObj = User.query.filter_by(username=username).first()
    if not (UserObj and check_password_hash(UserObj.password, login_creds['password'])):
        return jsonify(msg='Invalid Login Creds !'), 403
    login_user(UserObj)
    return jsonify(msg="Login Successfull !", username=UserObj.username), 200