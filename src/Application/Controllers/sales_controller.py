from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Service.sales_service import SaleService


class SaleController:
    @staticmethod
    def create_sale():

        seller_id = get_jwt_identity()  # Obtém o ID do seller autenticado
        data = request.json
        result, status_code = SaleService.create_sale(data, seller_id)
        return jsonify(result), status_code
