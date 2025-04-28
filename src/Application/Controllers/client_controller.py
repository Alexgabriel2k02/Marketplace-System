from flask import request, jsonify
from src.Application.Service.client_service import ClientService
from flask_jwt_extended import create_access_token

class ClientController:
    @staticmethod
    def create_client():
        body = request.get_json()
        result, status_code = ClientService.create_client(body)
        return jsonify(result), status_code

    @staticmethod
    def list_clients():
        clients = ClientService.list_clients()
        return jsonify(clients), 200

    @staticmethod
    def login_client(email, password):
        user = ClientService.authenticate(email, password)
        if user:
            access_token = create_access_token(
                identity=user.id,
                additional_claims={"name": user.name, "status": user.status},
            )
            return jsonify(access_token=access_token), 200

        return jsonify({"mensagem": "Credenciais inválidas"}), 401
