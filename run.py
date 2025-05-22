from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.routes import init_routes
from src.config.data_base import init_db, db
from src.Infrastructure.Model.seller import Seller
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.sales import Sale
from src.Infrastructure.Model.orders import Order
from src.Infrastructure.Model.client import Client
from datetime import timedelta
import os

app = Flask(__name__, static_url_path='/uploads', static_folder='uploads')

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"  # 🔥 Trocar por chave segura
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

init_db(app)

with app.app_context():
    db.create_all()

init_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
