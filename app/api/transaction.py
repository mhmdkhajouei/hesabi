from flask import Blueprint, request, jsonify


def transaction_bp(services):

    bp = Blueprint('transaction', __name__, url_prefix='/api/transactions')
    transaction_service = services["transaction"]


    @bp.route('/', methods=['POST'])
    def add_transaction():
        data = request.json

        required = ['amount', 'transactions_type', 'transaction_date']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        try:
            transaction_service.add_transaction(
                amount=data['amount'],
                transactions_type=data['transactions_type'],
                transaction_date=data['transaction_date'],
                category_id=data.get('category_id'),
                note=data.get('note')
            )
            return jsonify({'message': 'Transaction added successfully'}), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 400


    @bp.route('/<int:transaction_id>', methods=['PUT'])
    def edit_transaction(transaction_id):
        data = request.json

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            transaction_service.edit_transaction(transaction_id, **data)
            return jsonify({'message': 'Transaction updated successfully'}), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400


    @bp.route('/<int:transaction_id>', methods=['DELETE'])
    def delete_transaction(transaction_id):
        try:
            transaction_service.delete_transaction(transaction_id)
            return jsonify({'message': 'Transaction deleted successfully'}), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    return bp