from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import execute_query

bp = Blueprint('teachers', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_teachers():
    teachers = execute_query(
        "SELECT * FROM teachers ORDER BY id DESC",
        fetch_all=True
    )
    return jsonify(teachers or []), 200

@bp.route('/<int:teacher_id>', methods=['GET'])
@jwt_required()
def get_teacher(teacher_id):
    teacher = execute_query(
        "SELECT * FROM teachers WHERE id = %s",
        (teacher_id,),
        fetch_one=True
    )
    
    if teacher:
        return jsonify(teacher), 200
    return jsonify({'error': 'Teacher not found'}), 404

@bp.route('/', methods=['POST'])
@jwt_required()
def create_teacher():
    data = request.get_json()
    
    teacher_id = execute_query(
        """INSERT INTO teachers (
            employee_id, first_name, last_name, phone, email, 
            qualification, hire_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (
            data['employee_id'], data['first_name'], data['last_name'],
            data['phone'], data['email'], data.get('qualification'),
            data['hire_date']
        ),
        commit=True
    )
    
    if teacher_id:
        return jsonify({'message': 'Teacher created', 'id': teacher_id}), 201
    return jsonify({'error': 'Failed to create teacher'}), 500
