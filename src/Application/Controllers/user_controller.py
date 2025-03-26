from flask import request, jsonify, Blueprint, make_response
import jwt
from datetime import datetime, timedelta
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def create_seller():
        data = request.json
        result = UserService.create_seller(data)
        if result:
            return make_response(jsonify({
                "mensagem": "Seller criado com sucesso"
            }), 200)
        else:
            return make_response(jsonify({
                "mensagem": "Falha ao criar seller"
            }), 400)

    @staticmethod
    def activate_seller():
        data = request.json
        result = UserService.activate_seller(data)
        if result:
            # Gera o token de acesso diretamente aqui
            secret_key = "sua_chave_secreta"  # Substitua por uma chave segura
            payload = {
                "user_id": result.get("user_id"),  # Certifique-se de que o `result` contém o ID do usuário
                "role": "seller",
                "exp": datetime.utcnow() + timedelta(hours=1)  # Token válido por 1 hora
            }
            access_token = jwt.encode(payload, secret_key, algorithm="HS256")

            return make_response(jsonify({
                "mensagem": "Seller ativado com sucesso",
                "access_token": access_token
            }), 200)
        else:
            return make_response(jsonify({
                "mensagem": "Falha ao ativar seller"
            }), 400)