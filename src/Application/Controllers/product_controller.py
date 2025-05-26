from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
import os
from src.Application.Service.product_service import ProductService

class ProductController:
    @staticmethod
    def create_product():
        seller_id = get_jwt_identity()

        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        status = request.form.get('status', 'activated')

        img_file = request.files.get('img')
        img_path = None

        if img_file:
            filename = secure_filename(img_file.filename)

            upload_folder = current_app.config['UPLOAD_FOLDER']
            img_full_path = os.path.join(upload_folder, filename)

            img_file.save(img_full_path)
            img_path = f'uploads/{filename}'

        data = {
            "name": name,
            "price": float(price) if price else None,
            "quantity": int(quantity) if quantity else None,
            "status": status,
            "img": img_path,
        }

        result, status_code = ProductService.create_product(data, seller_id)
        return jsonify(result), status_code

    @staticmethod
    def get_product_details(product_id):
        seller_id = get_jwt_identity()
        result, status_code = ProductService.get_product_details(product_id, seller_id)
        return jsonify(result), status_code
    
    @staticmethod
    def delete_product(product_id):
        seller_id = get_jwt_identity()
        result, status_code = ProductService.delete_product(product_id, seller_id)
        return jsonify(result), status_code

    @staticmethod
    def inactivate_product(product_id):
        seller_id = get_jwt_identity()
        result, status_code = ProductService.inactivate_product(product_id, seller_id)
        return jsonify(result), status_code

    @staticmethod
    def toggle_product_status(product_id):
        seller_id = get_jwt_identity()
        result, status_code = ProductService.toggle_product_status(product_id, seller_id)
        return jsonify(result), status_code    

    @staticmethod
    def list_products():
        seller_id = get_jwt_identity()
        result, status_code = ProductService.list_products(seller_id)
        return jsonify(result), status_code