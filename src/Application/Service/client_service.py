from src.Infrastructure.Model.client import Client
from src.config.data_base import db


class ClientService:
    @staticmethod
    def create_client(data):
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")

        
        if not all([name, email]):
            return {"mensagem": "Nome e e-mail são obrigatórios"}, 400

        if Client.query.filter_by(email=email).first():
            return {"mensagem": "E-mail já cadastrado"}, 400

        if Client.query.filter_by(phone=phone).first():
            return {"mensagem": "Telefone já cadastrado"}, 400

        
        client = Client(name=name, email=email, phone=phone)
        client.status = "Ativo"
        db.session.add(client)
        db.session.commit()

        return {"mensagem": "Cliente criado com sucesso"}, 201

    @staticmethod
    def list_clients():
        clients = Client.query.all()
        return [client.to_dict() for client in clients]

    @staticmethod
    def authenticate(email):
        client = Client.query.filter_by(email=email).first()

        if client:
            return client
        return None
