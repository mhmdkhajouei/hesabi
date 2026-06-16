from flask import request, Blueprint ,jsonify


def category_bp(services):

    bp = Blueprint("category", __name__, url_prefix="/api/categories")
    category_service = services["category"]


    @bp.route('/', methods=['POST'])
    def add_category():

        data = request.json
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400

        required = ['category_name']
        for field in required:
            if field not in data:
                return jsonify({'error': f'{field} is requied'}), 400

        try:
            category_service.add_category(
                category_name = data['category_name']
            )
            return jsonify({'message': 'Category added successfully'}), 201


        except ValueError as e:
            return jsonify({'error': str(e)}), 400


    @bp.route('/<int:category_id>', methods=['PUT'])
    def edit_category(category_id):

        data = request.json

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            category_service.edit_category(category_id,**data)
            return jsonify({'message': 'Category updated successfully'}), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400


    @bp.route('/<int:category_id>', methods=['DELETE'])
    def delete_category(category_id):

        try:
            category_service.delete_category(category_id)
            return jsonify({'message': 'Category selected deleted successfully'}), 200

        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    return bp