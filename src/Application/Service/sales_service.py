from src.Infrastructure.Model.sales import Sale
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.seller import Seller
from src.config.data_base import db


class SaleService:
    @staticmethod
    def create_sale(data, seller_id):
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        # verifica se product_id e quantity são válidos
        if not product_id or not isinstance(product_id, int):
            return {"mensagem": "ID do produto inválido ou não fornecido"}, 400

        if not quantity or not isinstance(quantity, int) or quantity <= 0:
            return {"mensagem": "Quantidade inválida ou não fornecida"}, 400

        # verifica se o seller está ativo
        seller = Seller.query.get(seller_id)
        if not seller or seller.status != "Ativo":
            return {"mensagem": "Seller inativo ou não encontrado"}, 403

        # verifica se o produto existe e está ativo
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return {"mensagem": "Produto inativo ou não encontrado"}, 400

        # verifica se há estoque suficiente
        if product.stock < quantity:
            return {"mensagem": "Estoque insuficiente"}, 400

        # registra a venda
        sale = Sale(
            product_id=product_id,
            seller_id=seller_id,
            quantity=quantity,
            price_at_sale=product.price,  # Preço no momento da venda
        )
        db.session.add(sale)

        # atualiza o estoque do produto
        product.stock -= quantity
        db.session.commit()

        return {"mensagem": "Venda registrada com sucesso", "sale_id": sale.id}, 201
