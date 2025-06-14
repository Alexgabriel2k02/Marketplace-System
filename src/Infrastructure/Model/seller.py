from src.config.data_base import db


class Seller(db.Model):
    __tablename__ = "sellers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=True)
    phone = db.Column(db.String(30),unique=True, nullable=True)
    status = db.Column(db.String(10), nullable=True, default="Inativo")
    verification_code = db.Column(db.String(4), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "cnpj": self.cnpj,
            "phone": self.phone,
            "status": self.status,
            "verification_code": self.verification_code,
        }
