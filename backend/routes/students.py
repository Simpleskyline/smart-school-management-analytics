from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import execute_query

bp = Blueprint('students', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_students():
    students = execute_query(
        "SELECT * FROM students ORDER BY id DESC",
        fetch_all=True
    )
    return jsonify(students or []), 200

@bp.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    student = execute_query(
        "SELECT * FROM students WHERE id = %s",
        (student_id,),
        fetch_one=True
    )
    
    if student:
        return jsonify(student), 200
    return jsonify({'error': 'Student not found'}), 404

@bp.route('/', methods=['POST'])
@jwt_required()
def create_student():
    data = request.get_json()
    
    student_id = execute_query(
        """INSERT INTO students (
            admission_number, first_name, last_name, date_of_birth, 
            gender, guardian_name, guardian_phone, enrollment_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            data['admission_number'], data['first_name'], data['last_name'],
            data['date_of_birth'], data['gender'], data.get('guardian_name'),
            data.get('guardian_phone'), data['enrollment_date']
        ),
        commit=True
    )
    
    if student_id:
        return jsonify({'message': 'Student created', 'id': student_id}), 201
    return jsonify({'error': 'Failed to create student'}), 500

@bp.route('/<int:student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    data = request.get_json()
    
    result = execute_query(
        """UPDATE students SET 
            first_name = %s, last_name = %s, phone = %s, 
            address = %s, status = %s
        WHERE id = %s""",
        (
            data['first_name'], data['last_name'], data.get('phone'),
            data.get('address'), data.get('status'), student_id
        ),
        commit=True
    )
    
    if result:
        return jsonify({'message': 'Student updated'}), 200
    return jsonify({'error': 'Failed to update'}), 500

@bp.route('/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    result = execute_query(
        "DELETE FROM students WHERE id = %s",
        (student_id,),
        commit=True
    )
    
    if result:
        return jsonify({'message': 'Student deleted'}), 200
    return jsonify({'error': 'Failed to delete'}), 500

