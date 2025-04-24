from src.config.data_base import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)  # Nome do cliente
    product_name = db.Column(db.String(100), nullable=False)  # Nome do produto
    quantity = db.Column(db.Integer, nullable=False)  # Quantidade do produto

    def to_dict(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "product_name": self.product_name,
            "quantity": self.quantity,
        }
