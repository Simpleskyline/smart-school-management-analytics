from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import execute_query

bp = Blueprint('classes', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_classes():
    classes = execute_query(
        """SELECT c.*, CONCAT(t.first_name, ' ', t.last_name) as teacher_name
        FROM classes c
        LEFT JOIN teachers t ON c.teacher_id = t.id
        ORDER BY c.id DESC""",
        fetch_all=True
    )
    return jsonify(classes or []), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_class():
    data = request.get_json()
    
    class_id = execute_query(
        """INSERT INTO classes (
            class_name, section, teacher_id, academic_year, capacity
        ) VALUES (%s, %s, %s, %s, %s)""",
        (
            data['class_name'], data.get('section'), data.get('teacher_id'),
            data['academic_year'], data.get('capacity', 30)
        ),
        commit=True
    )
    
    if class_id:
        return jsonify({'message': 'Class created', 'id': class_id}), 201
    return jsonify({'error': 'Failed to create class'}), 500
