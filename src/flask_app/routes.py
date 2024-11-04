# flask_app/routes.py
from flask import Blueprint, jsonify, request
from utils.dbcon import runQuery

main = Blueprint('main', __name__)


@main.route('/')
def get_home():
    data = {
        "message": "Hello from Flask!",
        "values": [1, 2, 3, 4, 5]
    }
    return jsonify(data)

@main.route('/auth')
def auth() -> bool:
    # Get username and password from the query parameters
    username = request.args.get('username')
    password = request.args.get('password')
    
    # Check if username and password were provided
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if the username and password are correct
    results = runQuery(f"SELECT * FROM users WHERE name = :name AND password = :password", {"name": username, "password": password})

    if len(results.all()) == 1:
        return jsonify({'message': 'Authentication successful'}), 200
    return jsonify({'error': 'Authentication failed'}), 401