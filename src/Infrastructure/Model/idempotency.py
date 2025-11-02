from src.config.data_base import db

class IdempotencyKey(db.Model):
    __tablename__ = "idempotency_keys"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False)
    response_json = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "response_json": self.response_json,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
