from src.config.data_base import db
from src.Infrastructure.Model.client import Client


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)  # Nome do produto
    quantity = db.Column(db.Integer, nullable=False)  # Quantidade do produto

    client = db.relationship('Client', backref=db.backref('orders', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "client": self.client.to_dict() if self.client else None,
            "product_name": self.product_name,
            "quantity": self.quantity,
        }
