from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from backend.app import db
from backend.app.models import User

user_routes = Blueprint('user_routes', __name__)

bcrypt = Bcrypt()

@user_routes.route('/register', methods=['POST'])
def register():
    try:
        # Get user data from the request
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"message": "Username already exists"}), 400

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user
        new_user = User(username=username, password=hashed_password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_routes.route('/login', methods=['POST'])
def login():
    try:
        # Get user data from the request
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # Find the user by username
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password, password):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

