from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from database import execute_query

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    user = execute_query(
        "SELECT * FROM users WHERE username = %s AND is_active = 1",
        (data['username'],),
        fetch_one=True
    )
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not bcrypt.checkpw(data['password'].encode(), user['password_hash'].encode()):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user['id'])
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    }), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = execute_query(
        "SELECT id, username, email, role FROM users WHERE id = %s",
        (user_id,),
        fetch_one=True
    )
    
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email, and password required'}), 400
    
    existing_user = execute_query(
        "SELECT * FROM users WHERE username = %s OR email = %s",
        (data['username'], data['email']),
        fetch_one=True
    )
    
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 409
    
    password_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
    
    execute_query(
        "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
        (data['username'], data['email'], password_hash, 'student')
    )
    
    return jsonify({'message': 'User registered successfully'}), 201