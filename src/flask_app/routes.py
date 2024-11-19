# flask_app/routes.py
from flask import Blueprint, json, jsonify, request
from utils.dbcon import Transaction, runQuery, convert_to_dict

main = Blueprint('main', __name__)


@main.route('/')
def get_home():
    data = {
        "message": "Hello from Flask!",
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
    sql_result = runQuery(f"SELECT * FROM users WHERE email = :email AND password = :password", {"email": username, "password": password})
    result = convert_to_dict(sql_result)

    if len(result)  == 1:
        return jsonify({'message': 'Authentication successful','user':json.dumps(result[0])}), 200
    return jsonify({'error': 'Authentication failed'}), 401

@main.route('/tenants/apt', methods=["GET"], endpoint="get_tenant_apartment")
def get_tenant_apt():
    query = '''
    SELECT apts.*, owners.user_id as owner_id, owners.name as owner_name, owners.phone as owner_phone, owners.email as owner_email, managers.user_id as manager_id, managers.name as manager_name, managers.phone as manager_phone, managers.email as manager_email
    FROM apartments apts
             JOIN users owners
                  ON apts.apt_owner = owners.user_id
             JOIN users managers
                  ON apts.apt_manager = managers.user_id
    WHERE apts.apt_tenant = :user_id
    '''
    sql_result = runQuery(query, {"user_id": request.args.get('user_id')})
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
    return result

@main.route('/tenants/available_apts_count', methods=["GET"], endpoint="get_available_apts_count")
def get_tenant_apt_count():
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

@main.route('/owner/get_brokers', methods=["GET"], endpoint="get_brokers")
def get_brokers():
    sql_result = runQuery("SELECT * FROM Users WHERE is_broker = True order by broker_successful_deals desc, name")
    result = convert_to_dict(sql_result)
    return jsonify(result)

@main.route('/owner/apt', methods=["GET"], endpoint="get_owner_apartment")
def get_owner_apt():
    sql_result = runQuery("SELECT Apartments.*, Users.name as manager_name, Users.email as manager_email, Users.phone as manager_phone, tenants.name as tenant_name, tenants.email as tenant_email, tenants.phone as tenant_phone"
                          " FROM Apartments INNER JOIN Users on Apartments.apt_manager = Users.user_id"
                          " LEFT JOIN Users tenants on Apartments.apt_tenant = tenants.user_id"
                          " WHERE apt_owner = :user_id order by suburb", {"user_id": request.args.get('user_id')})
    result = convert_to_dict(sql_result)
    return jsonify(result)

@main.route('/broker/apt', methods=["GET"], endpoint="get_broker_apartment")
def get_owner_apt():
    sql_result = runQuery("SELECT * FROM Apartments WHERE apt_manager = :user_id order by suburb", {"user_id": request.args.get('user_id')})
    result = convert_to_dict(sql_result)
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

@main.route('/tenants/create_offer', methods=["POST"], endpoint="create_offer")
def create_offer():
    apt_id = request.args.get('apt_id')
    tenant_id = request.args.get('tenant_id')

    if not apt_id or not tenant_id:
        return jsonify({'error': 'Missing details'}), 400

    sql_query = '''
    INSERT INTO offers (offered_price, duration, tenant_id, apt_id)
    VALUES 
    (:offered_price, :duration, :tenant_id, :apt_id)
    '''

    try:
        runQuery(sql_query, request.args)
        return jsonify({'message': 'Apartment deleted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to delete apartment'}), 500


@main.route('/user/get_offers', methods=["GET"], endpoint="get_offers")
def get_offers():
    query = '''
    select offers.*, apartments.apt_address
    from offers
    inner join
    apartments
    on apartments.apt_id = offers.apt_id
    where apartments.apt_manager = :user_id
    order by apartments.apt_id, offers.tenant_id, offers.offered_price desc, offers.duration desc
    '''
    sql_result = runQuery(query, {'user_id': request.args.get('user_id')})
    result = convert_to_dict(sql_result)
    return jsonify(result)

@main.route('/owner/delete_offer', methods=["DELETE"], endpoint="delete_offer")
def delete_offer():
    apt_id = request.args.get('apt_id')
    tenant_id = request.args.get('tenant_id')
    offer_id = request.args.get('offer_id')

    if not apt_id or not tenant_id or not offer_id:
        return jsonify({'error': 'Missing details'}), 400

    try:
        runQuery("DELETE FROM Offers WHERE apt_id = :apt_id and tenant_id = :tenant_id and offer_id = :offer_id",
                 {'apt_id': apt_id, 'tenant_id': tenant_id, 'offer_id': offer_id})
        return jsonify({'message': 'Offer deleted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to delete offer'}), 500


@main.route('/owner/accept_offer', methods=["POST"], endpoint="accept_offer")
def accept_offer():
    apt_id = request.args.get('apt_id')
    tenant_id = request.args.get('tenant_id')
    rented_date = request.args.get('rented_date')
    duration = request.args.get('duration')
    offered_price = request.args.get('offered_price')
    offer_id = request.args.get('offer_id')
    broker_id = request.args.get('broker_id')

    if not apt_id or not tenant_id or not rented_date or not duration or not offered_price or not offer_id:
        return jsonify({'error': 'Missing details'}), 400

    sql_query = '''
    UPDATE apartments
    SET
        apt_rent = :offered_price,
        apt_rented_date = :rented_date,
        apt_rented_duration = :duration,
        apt_tenant = :tenant_id
    WHERE
        apt_id = :apt_id;
    '''

    update_broker_successful_deals = '''
    UPDATE users
    SET broker_successful_deals = broker_successful_deals + 1
    WHERE user_id = :broker_id;
    '''

    try:
        runQuery(sql_query, {'apt_id': apt_id, 'tenant_id': tenant_id, 'duration': duration, 'offered_price': offered_price, 'rented_date': rented_date})
        runQuery("DELETE FROM Offers WHERE apt_id = :apt_id or tenant_id = :tenant_id",
                 {'apt_id': apt_id, 'tenant_id': tenant_id})
        if broker_id:
            runQuery(update_broker_successful_deals, {'broker_id': broker_id})
        return jsonify({'message': 'Offer accepted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to accept offer'}), 500


@main.route('/user/', methods=["POST"], endpoint="create_user")
def create_user():
    try:
        runQuery("INSERT INTO Users (name, password, email, phone, is_owner, is_broker, is_tenant, is_repairmen, broker_successful_deals) VALUES (:name, :password, :email, :phone, :is_owner, :is_broker, :is_tenant, :is_repairmen, :broker_successful_deals)", request.get_json())
        sql_result = runQuery(f"SELECT * FROM users WHERE email = :email AND password = :password",
                              {"email": request.get_json()['email'], "password": request.get_json()['password']})
        result = convert_to_dict(sql_result)
        return jsonify({'message': 'User created successfully', 'user': result[0]}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to create user'}), 500


@main.route('/tenant/report_issue', methods=["POST"], endpoint="create_issue")
def create_issue():
    try:
        runQuery("INSERT INTO maintenance_issues (apt_id, issue_description, issue_date) VALUES (:apt_id, :issue, :issue_date)", request.get_json())
        return jsonify({'message': 'Issue reported successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to report issue'}), 500

@main.route('/tenant/issues', methods=["GET"], endpoint="get_issues")
def get_issue():
    sql_result = runQuery("SELECT * FROM maintenance_issues WHERE apt_id = :apt_id", {"apt_id": request.args.get('apt_id')})
    result = convert_to_dict(sql_result)
    return jsonify(result)

@main.route('/tenant/appointments', methods=["GET"], endpoint="get_appointments")
def get_appointments():
    sql_result = runQuery("SELECT * FROM appointments WHERE apt_id = :apt_id", {"apt_id": request.args.get('apt_id')})
    result = convert_to_dict(sql_result)
    return jsonify(result)

@main.route('/repairmen/appointments', methods=["GET"], endpoint="get_repairmen_appointments")
def get_repairmen_appointments():
    sql_result = runQuery("SELECT * FROM appointments WHERE repairmen_id = :repairmen_id", {"repairmen_id": request.args.get('repairmen_id')})
    result = convert_to_dict(sql_result)
    return jsonify(result)

@main.route('/repairmen/issues', methods=["GET"], endpoint="get_repairmen_issues")
def get_all_issues():
    sql_result = runQuery("SELECT * FROM maintenance_issues as mi where not exists (select * from appointments as a where a.issue_id = mi.issue_id ) order by issue_date desc")
    result = convert_to_dict(sql_result)
    return jsonify(result)

@main.route('/repairmen/commit', methods=["POST"], endpoint="repairmen_commit")
def commit_repairmen():
    try:
        runQuery("INSERT INTO appointments (apt_id, repairmen_id, issue_id, appointment_date, duration, charges) VALUES (:apt_id, :repairmen_id, :issue_id, :appointment_date, :duration, :charges)", request.get_json())
        return jsonify({'message': 'Appointment scheduled successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to schedule appointment'}), 500

@main.route('/tenant/resolve', methods=["DELETE"], endpoint="delete_appointment")
def delete_appointment():
    apt_id = request.args.get('apt_id')
    appointment_id = request.args.get('appointment_id')
    issue_id = request.args.get('issue_id')
    if not (apt_id and issue_id and appointment_id):
        return jsonify({'error': 'Missing details'}), 400
    try:
        transaction:Transaction = Transaction()
        transaction.runQuery("DELETE FROM appointments WHERE apt_id = :apt_id and appointment_id = :appointment_id", {"apt_id": apt_id, "appointment_id": appointment_id})
        transaction.runQuery("DELETE FROM maintenance_issues WHERE apt_id = :apt_id and issue_id = :issue_id", {"apt_id": apt_id, "issue_id": issue_id})
        transaction.commit()
        return jsonify({'message': 'Appointment scheduled successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to schedule appointment'}), 500

@main.route('/tenant/get_chats', methods=["GET"], endpoint="get_tenant_chats")
def get_tenant_chats():
    query = '''
    select *
    from chat
    inner join 
    apartments as apt
    on chat.apt_id = apt.apt_id
    where chat.tenant_id = :tenant_id
    order by chat.apt_id
    '''
    sql_result = runQuery(query, {'tenant_id': request.args.get('tenant_id')})
    result = convert_to_dict(sql_result)
    return jsonify(result)

@main.route('/manager/get_chats', methods=["GET"], endpoint="get_manager_chats")
def get_manager_chats():
    query = '''
    select *
    from chat
    inner join 
    apartments as apt
    on chat.apt_id = apt.apt_id
    where apt.apt_manager = :manager_id
    order by chat.apt_id, chat.tenant_id
    '''
    sql_result = runQuery(query, {'manager_id': request.args.get('manager_id')})
    result = convert_to_dict(sql_result)
    return jsonify(result)

@main.route('/tenant/get_chat_by_apt', methods=["GET"], endpoint="get_chat_by_apt")
def get_chats():
    query = '''
    select *
    from chat
    inner join 
    apartments as apt
    on chat.apt_id = apt.apt_id
    where chat.tenant_id = :tenant_id and chat.apt_id = :apt_id
    order by chat.apt_id
    '''
    sql_result = runQuery(query, request.args)
    result = convert_to_dict(sql_result)
    return jsonify(result)

@main.route('/tenant/get_messages', methods=["GET"], endpoint="get_messages")
def get_messages():
    query = '''
    select *
    from messages
    where chat_id = :chat_id and apt_id = :apt_id
    order by sent_time
    '''
    sql_result = runQuery(query, request.args)
    result = convert_to_dict(sql_result)
    return jsonify(result)

@main.route('/tenant/send_message', methods=["POST"], endpoint="send_message")
def send_message():
    apt_id = request.args.get('apt_id')
    chat_id = request.args.get('chat_id')
    content = request.args.get('content')
    is_from_tenant = request.args.get('is_from_tenant')

    if not apt_id or not chat_id or not content or is_from_tenant is None:
        return jsonify({'error': 'Missing details'}), 400

    sql_query = '''
    INSERT INTO messages (content, sent_time, apt_id, chat_id, is_from_tenant)
    VALUES 
    (:content, NOW(), :apt_id, :chat_id, :is_from_tenant)
    '''

    try:
        runQuery(sql_query, {
            'content': content,
            'apt_id': apt_id,
            'chat_id': chat_id,
            'is_from_tenant': is_from_tenant
        })
        return jsonify({'message': 'Message added successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to add message'}), 500

@main.route('/tenant/create_chat', methods=["POST"], endpoint="create_chat")
def create_chat():
    apt_id = request.args.get('apt_id')
    tenant_id = request.args.get('tenant_id')

    if not apt_id or not tenant_id:
        return jsonify({'error': 'Missing details'}), 400

    sql_query = '''
    INSERT INTO chat (apt_id, tenant_id)
    VALUES 
    (:apt_id, :tenant_id)
    '''

    try:
        runQuery(sql_query, {
            'apt_id': apt_id,
            'tenant_id': tenant_id,
        })
        return jsonify({'message': 'Chat created successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to create chat'}), 500
