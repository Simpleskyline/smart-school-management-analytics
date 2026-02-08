from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from database import execute_query

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = execute_query(
            "SELECT role FROM users WHERE id = %s",
            (user_id,),
            fetch_one=True
        )
        
        if not user or user['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper
