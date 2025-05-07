from src.Infrastructure.Model.seller import Seller
from src.config.data_base import db
from src.Infrastructure.http.whats_app import (
    send_verification_code,
    generate_activation_code,
)


class SellerService:
    @staticmethod
    def create_seller(data):
        name = data.get("name")
        cnpj = data.get("cnpj")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")

        # Validações
        if not all([name, cnpj, email, phone, password]):
            return {"mensagem": "Todos os campos são obrigatórios"}, 400

        if Seller.query.filter_by(email=email).first():
            return {"mensagem": "E-mail já cadastrado"}, 400

        if Seller.query.filter_by(cnpj=cnpj).first():
            return {"mensagem": "CNPJ já cadastrado"}, 400

        if Seller.query.filter_by(phone=phone).first():
            return {"mensagem": "Telefone já cadastrado"}, 400

        # Cria o vendedor
        user = Seller(name=name, cnpj=cnpj, email=email, phone=phone, password=password)
        user.verification_code = generate_activation_code()
        db.session.add(user)
        db.session.commit()

        # Envia o código de verificação
        send_verification_code([phone], user.verification_code)

        return {"mensagem": "Vendedor criado com sucesso"}, 201

    @staticmethod
    def activate_seller(data):
        phone_number = data.get("phone")
        verification_code = data.get("code")

        # Verificar se o vendedor existe
        user = Seller.query.filter_by(phone=phone_number).first()
        if not user:
            return {"mensagem": "Vendedor não encontrado"}, 404

        # Verificar o código de verificação
        if str(user.verification_code) != str(verification_code):
            return {"mensagem": "Código de verificação inválido"}, 400

        # Ativar o vendedor
        user.status = "Ativo"
        db.session.commit()

        return {"mensagem": "Vendedor ativado com sucesso"}, 200

    @staticmethod
    def authenticate(email, password):
        user = Seller.query.filter_by(email=email).first()

        if user and user.password == password:  # Substituir por hashing depois
            return user

        return None
