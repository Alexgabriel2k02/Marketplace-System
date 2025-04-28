from src.Infrastructure.Model.client import Client
from src.config.data_base import db


class ClientService:
    @staticmethod
    def create_client(data):
        nome = data.get("nome")
        email = data.get("email")
        celular = data.get("celular")

        if not all([nome, email]):
            return {"mensagem": "Nome e e-mail são obrigatórios"}, 400

        if Client.query.filter_by(email=email).first():
            return {"mensagem": "E-mail já cadastrado"}, 400

        if Client.query.filter_by(phone=celular).first():
            return {"mensagem": "Telefone já cadastrado"}, 400

        client = Client(name=nome, email=email, phone=celular)
        client.status = "Ativo"
        db.session.add(client)
        db.session.commit()

        return {"mensagem": "Cliente criado com sucesso"}, 201

    @staticmethod
    def list_clients():
        clients = Client.query.all()
        return [client.to_dict() for client in clients]

    @staticmethod
    def authenticate(email, password):
        client = Client.query.filter_by(email=email).first()
        # Como não temos senha no modelo Client, vamos assumir autenticação simples por email
        if client:
            return client
        return None
