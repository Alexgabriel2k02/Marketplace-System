from src.config.data_base import db

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    gateway_id = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    payload = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "method": self.method,
            "status": self.status,
            "gateway_id": self.gateway_id,
            "amount": self.amount,
            "payload": self.payload,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
