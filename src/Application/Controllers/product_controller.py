from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Service.product_service import ProductService


class ProductController:
    @staticmethod
    def create_product():

        seller_id = get_jwt_identity()  # pega o id do vendedor autenticado
        data = request.json
        result, status_code = ProductService.create_product(data, seller_id)
        return jsonify(result), status_code

    @staticmethod
    def list_products():

        seller_id = get_jwt_identity()
        products = ProductService.list_products(seller_id)
        return jsonify(products), 200

    @staticmethod
    def update_product(product_id):

        seller_id = get_jwt_identity()
        data = request.json
        result, status_code = ProductService.update_product(product_id, data, seller_id)
        return jsonify(result), status_code

    @staticmethod
    def get_product_details(product_id):

        seller_id = get_jwt_identity()
        result, status_code = ProductService.get_product_details(product_id, seller_id)
        return jsonify(result), status_code

    @staticmethod
    def inactivate_product(product_id):

        seller_id = get_jwt_identity()
        result, status_code = ProductService.inactivate_product(product_id, seller_id)
        return jsonify(result), status_code
