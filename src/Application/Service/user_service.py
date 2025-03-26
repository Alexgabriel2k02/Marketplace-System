from src.Infrastructure.Model.user import User
from src.config.data_base import db
from src.Infrastructure.http.whats_app import send_verification_code, generate_activation_code

class UserService:
    @staticmethod
    def create_seller(data):
        """
        Lógica para criar um seller.
        """
        nome = data.get('nome')
        cnpj = data.get('cnpj')
        email = data.get('email')
        celular = data.get('celular')
        senha = data.get('senha')

        if nome and cnpj and email and celular and senha:
            user = User(name=nome, cnpj=cnpj, email=email, phone=celular, password=senha)
            user.verification_code = generate_activation_code()
            db.session.add(user)
            db.session.commit()
            # Enviar código de verificação via WhatsApp
            send_verification_code([celular], user.verification_code)
            return True
        return False

    @staticmethod
    def activate_seller(data):
        """
        Lógica para ativar um seller.
        """
        phone_number = data.get('celular')
        verification_code = data.get('codigo')
        user = User.query.filter_by(phone=phone_number).first()
        if user and user.verification_code == verification_code:
            user.status = "Ativo"
            db.session.commit()
            return True
        return False