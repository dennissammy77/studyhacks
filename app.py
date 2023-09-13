from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
client = MongoClient("mongodb+srv://userxyz:userxyz@cluster0.5be8y.mongodb.net/?retryWrites=true&w=majority")  # Update with your MongoDB URI
db = client["studyhacks"]
collection = db["chats"]
@app.route('/')
def index():
    return "<h1> hello world</h1>"


# Create a new chat
@app.route("/chats", methods=["POST"])
def create_chat():
    print(request.content_type)
    data = request.get_json()
    chat_id = collection.insert_one(data).inserted_id
    return jsonify({"message": "Chat created successfully", "chat_id": str(chat_id)}), 201


@app.route("/chats", methods=["GET"])
def get_chats():
    chats = list(collection.find())
    
    # Convert ObjectId fields to strings
    for chat in chats:
        chat["_id"] = str(chat["_id"])
    
    return jsonify(chats), 200


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
