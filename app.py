#!/usr/bin/python3

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo
import bcrypt
import jwt
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = "a90ef4c3c5f40457616af79fd12283cd"
app.config['MONGO_URI'] = "mongodb://localhost:27017/jobhubSA"

mongo = PyMongo(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login_signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        email = data['email']
        password = data['password']

        # Check if the user already exists in the MongoDB collection
        user = mongo.db.users.find_one({"username": username})
        if user:
            return jsonify({'message': 'Username already exists!'}), 400

        # Hash the password and insert the new user
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        })

        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/login_signup', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']

        # Find the user in the MongoDB collection
        user = mongo.db.users.find_one({"username": username})
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'message': 'Invalid credentials!'}), 401

        # Create the JWT token
        token = jwt.encode({
            'username': user['username'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return redirect(url_for('dashboard', token=token))

    return render_template('login_signup.html')

@app.route('/dashboard')
@token_required
def dashboard(current_user):
    return render_template('dashboard.html', current_user=current_user)

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

@app.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    if current_user != 'admin':
        return jsonify({'message': 'Admin access required!'}), 403
    
    # Fetch all users from the MongoDB collection
    users = mongo.db.users.find({}, {"_id": 0, "username": 1, "email": 1})
    users_list = [{'username': user['username'], 'email': user['email']} for user in users]
    return jsonify(users_list), 200

if __name__ == '__main__':
    app.run(debug=True)

