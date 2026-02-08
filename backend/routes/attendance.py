from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import execute_query
from datetime import date

bp = Blueprint('attendance', __name__)

@bp.route('/mark', methods=['POST'])
@jwt_required()
def mark_attendance():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    attendance_id = execute_query(
        """INSERT INTO attendance (
            student_id, class_id, date, status, remarks, marked_by
        ) VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE status = %s, remarks = %s""",
        (
            data['student_id'], data['class_id'], data.get('date', date.today()),
            data['status'], data.get('remarks'), user_id,
            data['status'], data.get('remarks')
        ),
        commit=True
    )
    
    return jsonify({'message': 'Attendance marked'}), 200

@bp.route('/class/<int:class_id>', methods=['GET'])
@jwt_required()
def get_class_attendance(class_id):
    date_param = request.args.get('date', date.today())
    
    attendance = execute_query(
        """SELECT a.*, CONCAT(s.first_name, ' ', s.last_name) as student_name
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE a.class_id = %s AND a.date = %s""",
        (class_id, date_param),
        fetch_all=True
    )
    
    return jsonify(attendance or []), 200

@bp.route('/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_attendance(student_id):
    attendance = execute_query(
        """SELECT * FROM attendance 
        WHERE student_id = %s 
        ORDER BY date DESC LIMIT 30""",
        (student_id,),
        fetch_all=True
    )
    
    return jsonify(attendance or []), 200

