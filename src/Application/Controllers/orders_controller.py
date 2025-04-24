from flask import request, jsonify, make_response
from src.Application.Service.order_service import OrderService


class OrderController:
    @staticmethod
    def create_order():
        data = request.json
        result, status = OrderService.create_order(data)
        return make_response(jsonify(result), status)

    @staticmethod
    def list_orders():
        orders = OrderService.list_orders()
        return make_response(jsonify(orders), 200)

    @staticmethod
    def delete_order(order_id):
        result, status = OrderService.delete_order(order_id)
        return make_response(jsonify(result), status)
