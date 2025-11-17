from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Service.sales_service import SaleService


class SaleController:
    @staticmethod
    def create_sale():

        seller_id = get_jwt_identity()  # Obtém o ID do seller autenticado
        data = request.get_json()  
        result, status_code = SaleService.create_sale(data, seller_id)
        return jsonify(result), status_code

    @staticmethod
    def list_sales():
        result, status_code = SaleService.list_sales()
        return jsonify(result), status_code

    @staticmethod
    def get_sales_history():
        """Retorna o histórico de vendas com filtros opcionais"""
        seller_id = get_jwt_identity()
        
        # Parâmetros de filtro opcionais
        date_from = request.args.get("date_from", None)
        date_to = request.args.get("date_to", None)
        product_id = request.args.get("product_id", None)
        min_value = request.args.get("min_value", None)
        max_value = request.args.get("max_value", None)
        
        result, status_code = SaleService.get_sales_history(
            seller_id=seller_id,
            date_from=date_from,
            date_to=date_to,
            product_id=product_id,
            min_value=min_value,
            max_value=max_value
        )
        return jsonify(result), status_code

    @staticmethod
    def realizar_venda():
        data = request.get_json()
        order_id = data.get("order_id")
        # ...outros dados...
        return SaleService.realizar_venda(order_id, ...)
