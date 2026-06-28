from flask import request, Blueprint ,jsonify


def category_bp(services):

    bp = Blueprint("category", __name__, url_prefix="/api/categories")
    category_service = services["category"]

    @bp.route('/', methods=['GET'])
    def get_all_categories():
        try:
            result = category_service.get_all_categories()
            return jsonify({'data': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/', methods=['POST'])
    def add_category():

        data = request.json
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400

        required = ['category_name', 'budget_goal']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is requied'}), 400

        try:
            new_record = category_service.add_category(
                category_name = data['category_name'],
                budget_goal = data['budget_goal']
            )
            return jsonify({'message': 'Category added successfully', 'data': new_record}), 201


        except ValueError as e:
            return jsonify({'error': str(e)}), 400


    @bp.route('/<int:category_id>', methods=['PUT'])
    def edit_category(category_id):

        data = request.json

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            updated_record = category_service.edit_category(category_id,**data)
            return jsonify({'message': 'Category updated successfully', 'data': updated_record}), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400


    @bp.route('/<int:category_id>', methods=['DELETE'])
    def delete_category(category_id):

        try:
            deleted_id = category_service.delete_category(category_id)
            return jsonify({'message': 'Category selected deleted successfully', 'data': deleted_id}), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    return bp