from flask import Flask, jsonify, request, session
from models import *
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '829dbb1fb94a0c7156bad660fd43ef45'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ankita_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def create_db():
    with app.app_context():
        db.create_all()

@app.route('/api/v1/index', methods=['GET'])
def index():
    return jsonify(msg='this is my name', name='Anikta Roy'), 200

@app.route('/api/v1/context', methods=['GET'])
def context():
    return jsonify(classroom='special',topic='electrical'),200

@app.route('/api/v1/return-name', methods=['POST'])
def return_name_post():
    name = request.get_json()['name']
    return jsonify(name=name, msg='name returned !'), 200

@app.route('/api/v1/return-stream',methods=['POST'])
def return_details():
    data = request.get_json()
    name=data['name']
    section=data['section']
    return jsonify(name=name,section=section),200

@app.route('/api/v1/return-calculator',methods=['POST'])
def return_result():
    data=request.get_json()
    variable1=float (data['variable_a'])
    variable2=float(data['variable_b'])
    operator=data['operator']
    if(operator=='+'):
        return jsonify(result=(variable1+variable2)),200
    if(operator=='-'):
        return jsonify(result=(variable1-variable2)),200
    if(operator=='*'):
        return jsonify(result=(variable1*variable2)),200
    if (operator=='/'):
        return jsonify(result=(variable1/variable2)),200

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login_post'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
if __name__ == '__main__':
    app.debug = True
    app.run()