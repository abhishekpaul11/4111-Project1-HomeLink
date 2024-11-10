# flask_app/routes.py
from flask import Blueprint, json, jsonify, request
from utils.dbcon import runQuery, convert_to_dict

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
    sql_result = runQuery(f"SELECT * FROM users WHERE name = :name AND password = :password", {"name": username, "password": password})
    result = convert_to_dict(sql_result)

    if len(result)  == 1:
        return jsonify({'message': 'Authentication successful','user':json.dumps(result[0])}), 200
    return jsonify({'error': 'Authentication failed'}), 401

@main.route('/tenants/apt', methods=["GET"], endpoint="get_tenant_apartment")
def get_tenant_apt():
    sql_result = runQuery("SELECT a.* FROM Users as u, Apartments as a WHERE u.user_id = a.apt_tenant and u.user_id = :user_id", {"user_id": request.args.get('user_id')})
    result = convert_to_dict(sql_result)
    if len(result) == 0:
        return ""
    return jsonify(result[0])

@main.route('/tenants/available_apts', methods=["GET"], endpoint="get_available_apts")
def get_tenant_apt():
    query = '''
    SELECT apts.*, owners.user_id as owner_id, owners.name as owner_name, owners.phone as owner_phone, owners.email as owner_email, managers.user_id as manager_id, managers.name as manager_name, managers.phone as manager_phone, managers.email as manager_email
    FROM apartments apts
             JOIN users owners
                  ON apts.apt_owner = owners.user_id
             JOIN users managers
                  ON apts.apt_manager = managers.user_id
    WHERE apts.apt_tenant IS NULL
    ORDER BY apts.suburb, apts.apt_id
    LIMIT 10
        OFFSET :offset;
    '''
    sql_result = runQuery(query,
                          {"offset": request.args.get('offset')})
    result = convert_to_dict(sql_result)
    if len(result) == 0:
        return ""
    return result

@main.route('/tenants/available_apts_count', methods=["GET"], endpoint="get_available_apts_count")
def get_tenant_apt():
    query = '''
    SELECT count(*)
    FROM apartments apts
    WHERE apts.apt_tenant IS NULL
    '''
    sql_result = runQuery(query)
    result = convert_to_dict(sql_result)
    if len(result) == 0:
        return ""
    return result[0]


@main.route('/owner/apt', methods=["GET"], endpoint="get_owner_apartment")
def get_owner_apt():
    sql_result = runQuery("SELECT * FROM Apartments WHERE apt_owner = :user_id order by apt_id desc", {"user_id": request.args.get('user_id')})
    result = convert_to_dict(sql_result)
    if len(result) == 0:
        return ""
    return jsonify(result)

@main.route('/owner/create_apartment', methods=["POST"], endpoint="create_apartment")
def create_apt():
    apt_address = request.args.get('apt_address')
    apt_rent = request.args.get('apt_rent')
    apt_rooms = request.args.get('apt_rooms')
    suburb = request.args.get('suburb')
    distance_frm_fin = request.args.get('distance_frm_fin')
    apt_owner = request.args.get('apt_owner')
    apt_manager = request.args.get('apt_manager')

    try:
       runQuery("INSERT INTO Apartments (apt_address, apt_rent, apt_rooms, suburb, distance_frm_fin, apt_owner, apt_manager) VALUES (:apt_address, :apt_rent, :apt_rooms, :suburb, :distance_frm_fin, :apt_owner, :apt_manager)", {"apt_address": apt_address, "apt_rent": apt_rent, "apt_rooms": apt_rooms, "suburb": suburb, "distance_frm_fin": distance_frm_fin, "apt_owner": apt_owner, "apt_manager": apt_manager})
       return jsonify({'message': 'Apartment created successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to create apartment'}), 500

@main.route('/owner/delete_apartment', methods=["DELETE"], endpoint="delete_apartment")
def delete_apt():
    apt_id = request.args.get('apt_id')

    if not apt_id:
        return jsonify({'error': 'Apartment ID is required'}), 400

    try:
        runQuery("DELETE FROM Apartments WHERE apt_id = :apt_id", {"apt_id": apt_id})
        return jsonify({'message': 'Apartment deleted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to delete apartment'}), 500
