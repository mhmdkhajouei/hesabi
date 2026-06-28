from flask import Flask
from flask_cors import CORS
from main import create_app
from api.transaction import transaction_bp
from api.category import category_bp
from api.budget import budget_bp
from api.compute import compute_bp

app = Flask(__name__)
CORS(app)

conn, services = create_app()

app.register_blueprint(transaction_bp(services))
app.register_blueprint(category_bp(services))
app.register_blueprint(budget_bp(services))
app.register_blueprint(compute_bp(services))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)