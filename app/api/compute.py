from flask import Blueprint,jsonify


def compute_bp(services):

    bp = Blueprint("compute", __name__, url_prefix="/api/compute")
    compute_service = services["compute"]


    @bp.route("/income", methods= ['GET'])
    def income_balance():

        try:
            result = compute_service.income_balance()
            return jsonify({'income': result or 0 }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route("/expense", methods= ['GET'])
    def expense_balance():

        try:
            result = compute_service.expense_balance()
            return jsonify({'expense': result or 0 }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/total', methods=['GET'])
    def total_balance():

        try:
            result = compute_service.total_balance()
            return jsonify({'total': result or 0 }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/categories/balance', methods=['GET'])
    def categoires_balance():

        try:
            result = compute_service.categories_balance()
            return jsonify({'categories_balance': result or []}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/category/<int:category_id>/balance', methods=['GET'])
    def category_balance(category_id):

        try:
            result = compute_service.category_balance(category_id)
            return jsonify({'category_balance': result or {}}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return bp