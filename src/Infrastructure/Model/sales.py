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
    created_at = db.Column(db.DateTime, default=db.func.now())  

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "seller_id": self.seller_id,
            "order_id" : self.order_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,  
            "total_price": self.total_price,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")  
        }
