from flask import Blueprint

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    # user registration logic
    pass

@user_routes.route('/login', methods=['POST'])
def login():
    # user login logic 
    pass

