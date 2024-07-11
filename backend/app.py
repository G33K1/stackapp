from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  
from os import environ
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)

  def json(self):
    return {'id': self.id,'name': self.name, 'email': self.email}
  
# db.create_all()

class LogUser(db.Model):
  __tablename__ = 'log_users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  password2 = db.Column(db.String(60), nullable=False)

  def json(self):
    return {'id': self.id,'name': self.name, 'email': self.email,  'password': self.password, 'password2': self.password2,}
  
db.create_all()

# create a test route
@app.route('/test', methods=['GET'])
def test():
  return jsonify({'message': 'The server is running'})

# create a user signup
@app.route('/api/flask/signup', methods=['POST'])
def Signup():

  for key, value in request.headers.items():
    logging.info(f"{key}: {value}")

  logging.info(request)
  logging.info("Hello here")
  try:
    logging.info("There is no prooblem")
    data = request.get_json()
    logging.info ("data detected and found1")
    logging.info(data)

    new_user = LogUser(name=data['name'], email=data['email'], password=data['password'], password2=data['password2'])
    logging.info ("data detected and found2")
    db.session.add(new_user)
    logging.info ("data detected and found3")
    db.session.commit()  
    logging.info ("data detected and found4")


    return make_response(jsonify({
      'id': new_user.id,
      'name': new_user.name,
      'email': new_user.email,
      'password': new_user.password,
      'password2': new_user.password2,
    }), 201)  

  except Exception as e:
    logging.info(e)
    return make_response(jsonify({'message': 'error creating user', 'error': str(e)}), 500)
  
# sign in log user
@app.route('/api/flask/login', methods=['POST'])
def Login():
  try:
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = LogUser.query.filter_by(email=email).first()
    logging.info("user found")

    if not email or not password:
      return make_response(jsonify({'error': 'Email and password are required'}), 400)

    else:
      # user = LogUser.query.filter_by(email=email).first()

      if user.email == email and user.password == password:
        return jsonify(email, password), 201

      else:
        return make_response(jsonify({'error': 'Incorrect credentials'}), 401)
      
  except Exception as e:
    return make_response(jsonify({'message': 'error getting users', 'error': str(e)}), 500)

# get a log user by id
# @app.route('/api/flask/signup/<id>', methods=['GET'])
# def get_LogUser(id):
#   try:
#     user = LogUser.query.filter_by(id=id).first() # get the first user with the id
#     if user:
#       return make_response(jsonify({'user': user.json()}), 200)
#     return make_response(jsonify({'message': 'user not found'}), 404) 
#   except Exception as e:
#     return make_response(jsonify({'message': 'error getting user', 'error': str(e)}), 500)
  
# update a user by id
# @app.route('/api/flask/log_user/<id>', methods=['PUT'])
# def update_LogUser(id):
#   try:
#     user = LogUser.query.filter_by(id=id).first()
#     if user:
#       data = request.get_json()
#       user.name = data['name']
#       user.email = data['email']
#       db.session.commit()
#       return make_response(jsonify({'message': 'user updated'}), 200)
#     return make_response(jsonify({'message': 'user not found'}), 404)  
#   except Exception as e:
#       return make_response(jsonify({'message': 'error updating user', 'error': str(e)}), 500)

# create a user
@app.route('/api/flask/users', methods=['POST'])
def create_user():
  try:
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()  

    return jsonify({
        'id': new_user.id,
        'name': new_user.name,
        'email': new_user.email
    }), 201  

  except Exception as e:
    return make_response(jsonify({'message': 'error creating user', 'error': str(e)}), 500)
  
# get all users
@app.route('/api/flask/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    users_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(users_data), 200
  except Exception as e:
    return make_response(jsonify({'message': 'error getting users', 'error': str(e)}), 500)
  
# get a user by id
@app.route('/api/flask/users/<id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first() # get the first user with the id
    if user:
      return make_response(jsonify({'user': user.json()}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404) 
  except Exception as e:
    return make_response(jsonify({'message': 'error getting user', 'error': str(e)}), 500)
  
# update a user by id
@app.route('/api/flask/users/<id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.name = data['name']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)  
  except Exception as e:
      return make_response(jsonify({'message': 'error updating user', 'error': str(e)}), 500)

# delete a user by id
@app.route('/api/flask/users/<id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404) 
  except Exception as e:
    return make_response(jsonify({'message': 'error deleting user', 'error': str(e)}), 500)   
