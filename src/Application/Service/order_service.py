from src.Infrastructure.Model.orders import Order
from src.config.data_base import db


class OrderService:
    @staticmethod
    def create_order(data):
        cliente = data.get("cliente")
        produto = data.get("produto")
        quantidade = data.get("quantidade")

        if not cliente or not produto or not quantidade:
            return {"mensagem": "Todos os campos são obrigatórios"}, 400

        order = Order(cliente=cliente, produto=produto, quantidade=quantidade)
        db.session.add(order)
        db.session.commit()
        return {"mensagem": "Pedido criado com sucesso", "order": order.to_dict()}, 201

    @staticmethod
    def list_orders():
        orders = Order.query.all()
        return [order.to_dict() for order in orders]

    @staticmethod
    def delete_order(order_id):
        order = Order.query.get(order_id)
        if not order:
            return {"mensagem": "Pedido não encontrado"}, 404

        db.session.delete(order)
        db.session.commit()
        return {"mensagem": "Pedido excluído com sucesso"}, 200
