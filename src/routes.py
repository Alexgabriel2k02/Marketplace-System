from flask import Flask, jsonify, make_response, request, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS

from src.Application.Controllers.seller_controller import SellerController
from src.Application.Controllers.product_controller import ProductController
from src.Application.Controllers.sales_controller import SaleController
from src.Application.Controllers.orders_controller import OrderController
from src.Application.Controllers.client_controller import ClientController
from src.config.data_base import db


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'  # ajuste se necessário

    # Habilita CORS para o frontend
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

    # Rota para servir imagens
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route("/", methods=["GET"])
    def health():
        return make_response(
            jsonify({"mensagem": "API - OK; Docker - Up"}), 200
        )

    @app.route("/register/vendedores", methods=["POST"])
    def create_seller():
        return SellerController.create_seller()

    @app.route("/vendedores/activate", methods=["POST"])
    def activate_seller():
        return SellerController.activate_seller()

    @app.route("/auth/login", methods=["POST"])
    def login():
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        return SellerController.login(email, password)

    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected():
        current_user = get_jwt_identity()
        return jsonify({"mensagem": f"Bem-vindo, {current_user}! Esta é uma rota protegida."}), 200

    # Rotas produtos
    @app.route("/products", methods=["POST"])
    @jwt_required()
    def create_product():
        return ProductController.create_product()

    @app.route("/products", methods=["GET"])
    @jwt_required()
    def list_products():
        return ProductController.list_products()

    @app.route("/products/<int:product_id>", methods=["PUT"])
    @jwt_required()
    def update_product(product_id):
        return ProductController.update_product(product_id)

    @app.route("/products/<int:product_id>", methods=["GET"])
    @jwt_required()
    def get_product_details(product_id):
        return ProductController.get_product_details(product_id)

    @app.route("/products/<int:product_id>/inactivate", methods=["PATCH"])
    @jwt_required()
    def inactivate_product(product_id):
        return ProductController.inactivate_product(product_id)
    
    @app.route("/products/<int:product_id>", methods=["DELETE"])
    @jwt_required()
    def delete_product(product_id):
        return ProductController.delete_product(product_id)

    # Rotas vendas
    @app.route("/sales", methods=["POST"])
    @jwt_required()
    def create_sale():
        return SaleController.create_sale()

    # Rotas orders
    @app.route("/orders", methods=["POST"])
    @jwt_required()
    def create_order():
        return OrderController.create_order()

    @app.route("/orders", methods=["GET"])
    @jwt_required()
    def list_orders():
        return OrderController.list_orders()

    @app.route("/orders/<int:order_id>", methods=["GET"])
    @jwt_required()
    def get_order_details(order_id):
        return OrderController.get_order_details(order_id)

    @app.route("/orders/<int:order_id>", methods=["PUT"])
    @jwt_required()
    def update_order(order_id):
        return OrderController.update_order(order_id)

    @app.route("/orders/<int:order_id>", methods=["DELETE"])
    @jwt_required()
    def delete_order(order_id):
        return OrderController.delete_order(order_id)

    # Rotas client
    @app.route("/register/clients", methods=["POST"])
    def create_client():
        return ClientController.create_client()

    @app.route("/clients", methods=["GET"])
    def list_clients():
        return ClientController.list_clients()

    @app.route("/login/clients", methods=["POST"])
    def login_client():
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        return ClientController.login(email, password)

    @app.route("/sellers", methods=["GET", "OPTIONS"])
    def list_sellers():
        if request.method == "OPTIONS":
            return '', 200
        return SellerController.list_sellers()

    return app
