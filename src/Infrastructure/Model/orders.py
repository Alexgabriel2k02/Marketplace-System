from src.config.data_base import db
from src.Infrastructure.Model.client import Client
from src.Infrastructure.Model.product import Product  # Importe o modelo Product


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Adicione esta linha
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pendente")

    client = db.relationship('Client', backref=db.backref('orders', lazy=True))
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))  # Adicione esta linha

    def to_dict(self):
        return {
            "id": self.id,
            "client": self.client.to_dict() if self.client else None,
            "product": self.product.to_dict() if self.product else None,  # Retorna produto completo
            "quantity": self.quantity,
            "status": self.status
        }
