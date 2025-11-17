from src.config.data_base import db


class Sale(db.Model):
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)  
    total_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=True)  # Campo para data da venda (pode ser diferente de created_at)
    created_at = db.Column(db.DateTime, default=db.func.now())  

    # Relacionamento com Product
    product = db.relationship('Product', backref='sales')
    
    # Relacionamento com Seller
    seller = db.relationship('Seller', backref='sales')

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "seller_id": self.seller_id,
            "order_id": self.order_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,  
            "total_price": self.total_price,
            "date": (self.date or self.created_at).strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
