from src.config.data_base import db

# Relaciona com o seller


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Ativo")
    img = db.Column(db.String(255), nullable=True)
    seller_id = db.Column(
        db.Integer, db.ForeignKey("sellers.id"), nullable=False
    )  # Certifique-se de que "sellers.id" está correto

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "img": self.img,
            "seller_id": self.seller_id,
        }
