from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Initialize the MongoDB client and database
client = MongoClient("mongodb+srv://userxyz:userxyz@cluster0.5be8y.mongodb.net/?retryWrites=true&w=majority")
db = client["studyhacks"]
collection = db["chats"]
users_collection = db["users"]

# User registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    # Check if the user already exists
    existing_user = users_collection.find_one({'email': email})
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    # Generate a unique user ID
    user_id = str(ObjectId())

    # Hash the password before storing it
    hashed_password = generate_password_hash(password, method='sha256')

    # Create the user document
    user = {
        'user_id': user_id,
        'email': email,
        'password': hashed_password
    }

    # Insert the user document into the database
    users_collection.insert_one(user)

    return jsonify({'message': 'User registered successfully'}), 201

# User login
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = users_collection.find_one({'email': email})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful'}), 200

# Create a new chat
@app.route("/chats", methods=["POST"])
def create_chat():
    data = request.get_json()
    data['created_at'] = datetime.datetime.now()

    chat_id = collection.insert_one(data).inserted_id
    return jsonify({"message": "Chat created successfully", "chat_id": str(chat_id)}), 201

# Get all chats
@app.route("/chats", methods=["GET"])
def get_chats():
    chats = list(collection.find())
    
    # Convert ObjectId fields to strings
    for chat in chats:
        chat["_id"] = str(chat["_id"])
    
    return jsonify(chats), 200

# Get a specific chat by ID
@app.route("/chats/<string:chat_id>", methods=["GET"])
def get_chat(chat_id):
    chat = collection.find_one({"_id": ObjectId(chat_id)})
    if chat:
        # Convert ObjectId to string
        chat["_id"] = str(chat["_id"])
        return jsonify({"chat": chat}), 200
    else:
        return jsonify({"message": "Chat not found"}), 404

# Update a chat by ID
@app.route("/chats/<string:chat_id>", methods=["PUT"])
def update_chat(chat_id):
    data = request.get_json()
    result = collection.update_one({"_id": ObjectId(chat_id)}, {"$set": data})
    if result.modified_count == 1:
        return jsonify({"message": "Chat updated successfully"}), 200
    else:
        return jsonify({"message": "Chat not found"}), 404

# Delete a chat by ID
@app.route("/chats/<string:chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    result = collection.delete_one({"_id": ObjectId(chat_id)})
    if result.deleted_count == 1:
        return jsonify({"message": "Chat deleted successfully"}), 200
    else:
        return jsonify({"message": "Chat not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
