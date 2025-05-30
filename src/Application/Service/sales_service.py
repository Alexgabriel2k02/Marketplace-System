from src.Infrastructure.Model.sales import Sale
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.seller import Seller
from src.config.data_base import db


class SaleService:
    @staticmethod
    def create_sale(data, seller_id):
        product_id = data.get("product_id")
        quantity = data.get("quantity")


        # Validação do product_id
        if not product_id or not isinstance(product_id, int):
            return {"mensagem": "ID do produto inválido ou não fornecido"}, 400

        # Validação da quantidade
        if not quantity or not isinstance(quantity, int) or quantity <= 0:
            return {"mensagem": "Quantidade inválida ou não fornecida"}, 400

        # Validação do vendedor
        seller = Seller.query.get(seller_id)
        print(f"Vendedor encontrado: {seller}")
        if not seller or seller.status != "Ativo":
            return {"mensagem": "Seller inativo ou não encontrado"}, 403

        # Validação do produto e do seller_id
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        print(f"Produto encontrado: {product}")
        if not product or product.status != "Ativo":
            return {"mensagem": "Produto não encontrado ou não pertence ao vendedor"}, 404

        # Verificar estoque
        if product.quantity < quantity:
            return {"mensagem": "Estoque insuficiente"}, 400

        sale = Sale(
            product_id=product_id,
            seller_id=seller_id,
            quantity=quantity,
            unit_price=product.price,
            total_price=product.price * quantity,
        )
        db.session.add(sale)

        product.quantity -= quantity
        if product.quantity == 0:
            product.status = "Inativo"
        db.session.commit()

        print(f"Venda registrada com sucesso: sale_id={sale.id}")
        return {"mensagem": "Venda registrada com sucesso", "sale_id": sale.id}, 201

    @staticmethod
    def list_sales():
        sales = Sale.query.order_by(Sale.created_at.desc()).all()
        sales_list = [sale.to_dict() for sale in sales]
        return sales_list, 200
