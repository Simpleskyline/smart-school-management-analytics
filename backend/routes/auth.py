"""
Authentication routes - Login, Register, Logout
UPDATED VERSION WITH IMPROVED REGISTRATION
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import bcrypt
from datetime import datetime
import sys
sys.path.append('..')
from database import execute_query

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    """Register new user - UPDATED VERSION"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['firstName', 'lastName', 'username', 'email', 'password', 'role']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    # Validate password length
    if len(data['password']) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    
    # Validate username length
    if len(data['username']) < 3:
        return jsonify({'error': 'Username must be at least 3 characters long'}), 400
    
    # Validate email format
    import re
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate role
    valid_roles = ['student', 'teacher', 'admin']
    if data['role'].lower() not in valid_roles:
        return jsonify({'error': 'Invalid role. Must be student, teacher, or admin'}), 400
    
    # Check if username already exists
    existing_username = execute_query(
        "SELECT id FROM users WHERE username = %s",
        (data['username'],),
        fetch_one=True
    )
    
    if existing_username:
        return jsonify({'error': 'Username already exists'}), 409
    
    # Check if email already exists
    existing_email = execute_query(
        "SELECT id FROM users WHERE email = %s",
        (data['email'],),
        fetch_one=True
    )
    
    if existing_email:
        return jsonify({'error': 'Email already registered'}), 409
    
    try:
        # Hash password
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Insert user
        user_id = execute_query(
            "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (data['username'], data['email'], password_hash, data['role'].lower()),
            commit=True
        )
        
        if not user_id:
            return jsonify({'error': 'Failed to create user account'}), 500
        
        # If role is student or teacher, create corresponding record
        if data['role'].lower() == 'student':
            # Generate admission number (format: STU2024001)
            year = datetime.now().year
            # Get count of students for sequence number
            count_result = execute_query(
                "SELECT COUNT(*) as count FROM students",
                fetch_one=True
            )
            sequence = (count_result['count'] if count_result else 0) + 1
            admission_number = f"STU{year}{sequence:04d}"
            
            # Create student record
            execute_query(
                """INSERT INTO students 
                (user_id, admission_number, first_name, last_name, date_of_birth, gender, enrollment_date) 
                VALUES (%s, %s, %s, %s, %s, 'Other', %s)""",
                (
                    user_id, 
                    admission_number, 
                    data['firstName'], 
                    data['lastName'],
                    '2000-01-01',  # Default DOB, can be updated later
                    datetime.now().date()
                ),
                commit=True
            )
        
        elif data['role'].lower() == 'teacher':
            # Generate employee ID (format: T2024001)
            year = datetime.now().year
            count_result = execute_query(
                "SELECT COUNT(*) as count FROM teachers",
                fetch_one=True
            )
            sequence = (count_result['count'] if count_result else 0) + 1
            employee_id = f"T{year}{sequence:03d}"
            
            # Create teacher record
            execute_query(
                """INSERT INTO teachers 
                (user_id, employee_id, first_name, last_name, phone, email, hire_date) 
                VALUES (%s, %s, %s, %s, '', %s, %s)""",
                (
                    user_id,
                    employee_id,
                    data['firstName'],
                    data['lastName'],
                    data['email'],
                    datetime.now().date()
                ),
                commit=True
            )
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'user': {
                'id': user_id,
                'username': data['username'],
                'email': data['email'],
                'role': data['role'].lower(),
                'firstName': data['firstName'],
                'lastName': data['lastName']
            }
        }), 201
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed. Please try again.'}), 500

@bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    # Get user
    user = execute_query(
        "SELECT * FROM users WHERE username = %s AND is_active = 1",
        (data['username'],),
        fetch_one=True
    )
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Verify password
    if not bcrypt.checkpw(data['password'].encode('utf-8'), user['password_hash'].encode('utf-8')):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Update last login
    execute_query(
        "UPDATE users SET last_login = %s WHERE id = %s",
        (datetime.now(), user['id']),
        commit=True
    )
    
    # Create tokens
    access_token = create_access_token(identity=user['id'])
    refresh_token = create_refresh_token(identity=user['id'])
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
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
    """Get current user details"""
    user_id = get_jwt_identity()
    
    user = execute_query(
        "SELECT id, username, email, role, created_at, last_login FROM users WHERE id = %s",
        (user_id,),
        fetch_one=True
    )
    
    if user:
        return jsonify(user), 200
    
    return jsonify({'error': 'User not found'}), 404

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({'access_token': access_token}), 200