from src.Infrastructure.Model.product import Product
from src.config.data_base import db


class ProductService:
    @staticmethod
    def create_product(data, seller_id):

        # Validações
        if not data.get("name") or not data.get("price") or not data.get("quantity"):
            return {
                "message": "Os campos 'name', 'price' e 'quantity' são obrigatórios"
            }, 400

        # Cria o produto
        product = Product(
            name=data["name"],
            price=data["price"],
            quantity=data["quantity"],
            status=data.get("status", "Ativo"),
            img=data.get("img"),
            seller_id=seller_id,
        )
        db.session.add(product)
        db.session.commit()
        return {
            "message": "Produto criado com sucesso",
        }, 201

    @staticmethod
    def list_products(seller_id):

        products = Product.query.filter_by(seller_id=seller_id).all()
        return [product.to_dict() for product in products]

    @staticmethod
    def update_product(product_id, data, seller_id):

        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            return {"message": "Produto não encontrado"}, 404

        # Atualiza os campos
        product.name = data.get("name", product.name)
        product.price = data.get("price", product.price)
        product.quantity = data.get("quantity", product.quantity)
        product.status = data.get("status", product.status)
        product.img = data.get("img", product.img)
        db.session.commit()
        return {
            "message": "Produto atualizado com sucesso",
            "product": product.to_dict(),
        }, 200

    @staticmethod
    def get_product_details(product_id, seller_id):

        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            return {"message": "Produto não encontrado"}, 404
        return product.to_dict(), 200

    @staticmethod
    def inactivate_product(product_id, seller_id):

        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            return {"message": "Produto não encontrado"}, 404

        product.status = "Inativo"
        db.session.commit()
        return {"message": "Produto inativado com sucesso"}, 200
