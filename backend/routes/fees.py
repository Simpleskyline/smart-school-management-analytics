
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import execute_query

bp = Blueprint('fees', __name__)

@bp.route('/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_fees(student_id):
    fees = execute_query(
        "SELECT * FROM fees WHERE student_id = %s ORDER BY due_date DESC",
        (student_id,),
        fetch_all=True
    )
    return jsonify(fees or []), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_fee():
    data = request.get_json()
    
    fee_id = execute_query(
        """INSERT INTO fees (
            student_id, academic_year, fee_type, amount, due_date
        ) VALUES (%s, %s, %s, %s, %s)""",
        (
            data['student_id'], data['academic_year'], data['fee_type'],
            data['amount'], data['due_date']
        ),
        commit=True
    )
    
    if fee_id:
        return jsonify({'message': 'Fee created', 'id': fee_id}), 201
    return jsonify({'error': 'Failed to create fee'}), 500

@bp.route('/payment', methods=['POST'])
@jwt_required()
def record_payment():
    data = request.get_json()
    
    payment_id = execute_query(
        """INSERT INTO fee_payments (
            fee_id, amount_paid, payment_date, payment_method, transaction_id
        ) VALUES (%s, %s, %s, %s, %s)""",
        (
            data['fee_id'], data['amount_paid'], data['payment_date'],
            data['payment_method'], data.get('transaction_id')
        ),
        commit=True
    )
    
    # Update fee status
    execute_query(
        """UPDATE fees SET status = 
        CASE 
            WHEN (SELECT SUM(amount_paid) FROM fee_payments WHERE fee_id = %s) >= amount THEN 'Paid'
            ELSE 'Partial'
        END
        WHERE id = %s""",
        (data['fee_id'], data['fee_id']),
        commit=True
    )
    
    if payment_id:
        return jsonify({'message': 'Payment recorded'}), 201
    return jsonify({'error': 'Failed to record payment'}), 500

