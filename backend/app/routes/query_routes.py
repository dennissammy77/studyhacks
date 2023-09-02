from flask import Blueprint

query_routes = Blueprint('query_routes', __name__)

@query_routes.route('/save-query', methods=['POST'])
def save_query():
   
    pass

@query_routes.route('/get-queries', methods=['GET'])
def get_queries():
    
    pass

