from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
import os
from src.Application.Service.product_service import ProductService
from src.Infrastructure.Model.seller import Seller
from src.Infrastructure.Model.orders import Order  # Adicione este import

class ProductController:
    @staticmethod
    def create_product():
        seller_id = get_jwt_identity()

        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')

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
    
    @staticmethod
    def copy_product(product_id):
        seller_id = get_jwt_identity()
        result, status_code = ProductService.copy_product(product_id, seller_id)
        return jsonify(result), status_code

    @staticmethod
    def update_product(product_id):
        seller_id = get_jwt_identity()
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            name = request.form.get('name')
            price = request.form.get('price')
            quantity = request.form.get('quantity')
            status = request.form.get('status')  
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
        else:
            data = request.get_json()
            if data is None:
                return jsonify({"mensagem": "JSON inválido ou não enviado"}), 400

        result, status_code = ProductService.update_product(product_id, data, seller_id)
        return jsonify(result), status_code

    @staticmethod
    def apply_discount(product_id):
        seller_id = get_jwt_identity()
        # Buscar o nome do vendedor pelo id
        seller = Seller.query.filter_by(id=seller_id).first()
        seller_name = seller.name if seller else "Desconhecido"
        result, status_code = ProductService.apply_discount(product_id, seller_name)
        return jsonify(result), status_code

    @staticmethod
    def list_products_for_sale():
        result, status_code = ProductService.list_products_for_sale()
        return jsonify(result), status_code
