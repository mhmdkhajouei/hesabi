from flask import request, Blueprint, jsonify


def budget_bp(services):

    bp = Blueprint("budget", __name__, url_prefix="/api/budgets")
    budget_service = services['budget']

    @bp.route('/', methods=['POST'])
    def add_budget():

        data = request.json
        if not data:
            return jsonify({'error': 'request body must be JSON'}), 400

        required = ['budget_goal','category_id']
        for field in required:
            if not field in data:
                return jsonify({'error': f'{field} is required'}), 400

        try:
            budget_service.add_budget(
                budget_goal = data['budget_goal'],
                category_id = data['category_id']
                )
            return jsonify({'message': 'Budget added successfully'}), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @bp.route('/<int:budget_id>', methods=['PUT'])
    def edit_budget(budget_id):

        data = request.json
        if not data:
            return jsonify({'error': 'request body must be JSON'}), 400

        try:
            budget_service.edit_budget(budget_id,**data)
            return jsonify({'message': 'Budget updated successfully '}),200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400


    @bp.route('/<int:budget_id>' ,methods=['DELETE'])
    def delete_budget(budget_id):

        try:
            budget_service.delete_budget(budget_id)
            return jsonify({'message': 'Budget selected deleted successfully'}), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    return bp