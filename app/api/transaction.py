from flask import Blueprint, request, jsonify


def transaction_bp(services):

    bp = Blueprint('transaction', __name__, url_prefix='/api/transactions')
    transaction_service = services["transaction"]

    @bp.route('/', methods=['GET'])
    def get_all_transactions():
        try:
            result = transaction_service.get_all_transactions()
            return jsonify({'data': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/', methods=['POST'])
    def add_transaction():
        data = request.json

        required = ['amount', 'transaction_type', 'transaction_date']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        try:
            new_record = transaction_service.add_transaction(
                amount=data['amount'],
                transaction_type=data['transaction_type'],
                transaction_date=data['transaction_date'],
                category_id=data.get('category_id'),
                note=data.get('note')
            )
            return jsonify({'message': 'Transaction added successfully', 'data': new_record}), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 400


    @bp.route('/<int:transaction_id>', methods=['PUT'])
    def edit_transaction(transaction_id):
        data = request.json

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            updated_record = transaction_service.edit_transaction(transaction_id, **data)
            return jsonify({'message': 'Transaction updated successfully', 'data': updated_record}), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400


    @bp.route('/<int:transaction_id>', methods=['DELETE'])
    def delete_transaction(transaction_id):
        try:
            deleted_id = transaction_service.delete_transaction(transaction_id)
            return jsonify({'message': 'Transaction deleted successfully', 'data': deleted_id}), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    return bp