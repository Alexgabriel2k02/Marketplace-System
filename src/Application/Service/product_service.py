from src.Infrastructure.Model.product import Product
from src.config.data_base import db


class ProductService:
    @staticmethod
    def create_product(data, seller_id):
        
        if not data.get("name") or not isinstance(data.get("price"), (int, float)) or data.get("price") <= 0 or not isinstance(data.get("quantity"), int) or data.get("quantity") <= 0:
            return {
                "mensagem": "Os campos 'name', 'price' e 'quantity' são obrigatórios e devem conter valores válidos"
            }, 400

        product = Product(
            name=data["name"],
            price=data["price"],
            quantity=data["quantity"],
            status="Ativo",
            img=data.get("img"),
            seller_id=seller_id,
        )
        db.session.add(product)
        db.session.commit()
        return {
            "mensagem": "Produto criado com sucesso",
        }, 201

    @staticmethod
    def list_products(seller_id):
        products = Product.query.filter_by(seller_id=seller_id).all()  
        return [product.to_dict() for product in products], 200

    @staticmethod
    def update_product(product_id, data, seller_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            return {"mensagem": "Produto não encontrado ou não pertence ao vendedor"}, 404


        product.name = data.get("name", product.name)
        product.price = data.get("price", product.price)
        product.quantity = data.get("quantity", product.quantity)
        product.status = data.get("status", product.status)

        # Só atualize a imagem se uma nova for enviada
        if "img" in data and data["img"] is not None:
            product.img = data["img"]

        db.session.commit()
        return {
            "mensagem": "Produto atualizado com sucesso",
            "produto": product.to_dict(),
        }, 200

    @staticmethod
    def get_product_details(product_id, seller_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            return {"mensagem": "Produto não encontrado ou não pertence ao vendedor"}, 404
        return product.to_dict(), 200

    @staticmethod
    def inactivate_product(product_id, seller_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            return {"mensagem": "Produto não encontrado ou não pertence ao vendedor"}, 404

        if product.status == "Inativo":
            return {"mensagem": "O produto já está inativo"}, 400

        product.status = "Inativo"
        db.session.commit()
        return {"mensagem": "Produto inativado com sucesso"}, 200

    @staticmethod
    def toggle_product_status(product_id, seller_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            return {"mensagem": "Produto não encontrado ou não pertence ao vendedor"}, 404

        # Padronize os status para "Ativo" e "Inativo"
        if product.status == "Ativo":
            product.status = "Inativo"
        else:
            product.status = "Ativo"
        db.session.commit()
        return {
            "mensagem": f"Status do produto alterado para {product.status}",
            "produto": product.to_dict(),
        }, 200


    @staticmethod
    def delete_product(product_id, seller_id):
        product = Product.query.filter_by(id=product_id, seller_id=seller_id).first()
        if not product:
            return {"mensagem": "Produto não encontrado ou não pertence ao vendedor"}, 404

        db.session.delete(product)
        db.session.commit()
        return {"mensagem": "Produto deletado com sucesso"}, 200
