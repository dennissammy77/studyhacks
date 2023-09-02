from flask import Blueprint, request, jsonify
from backend.app import db
from backend.app.models import Query
from flask_login import login_required, current_user
from huggingface_api import query 
from config import SECRET_KEY

query_routes = Blueprint('query_routes', __name__)

@query_routes.route('/save-query', methods=['POST'])
@login_required 
def save_query():
    try:
        data = request.json
        query_text = data.get('query_text')

        new_query = Query(user_id=current_user.id, query_text=query_text)
        db.session.add(new_query)
        db.session.commit()
        
        huggingface_response = query({"inputs": query_text}, SECRET_KEY)
        return jsonify({"message": "Query saved successfully", "huggingface_response": huggingface_response}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@query_routes.route('/get-queries', methods=['GET'])
@login_required 
def get_queries():
    try:
        queries = Query.query.filter_by(user_id=current_user.id).all()
        query_texts = [query.query_text for query in queries]

        return jsonify({"queries": query_texts}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
