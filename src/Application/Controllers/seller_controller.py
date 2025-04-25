from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token
from src.Application.Service.seller_service import SellerService
from src.Infrastructure.Model.seller import Seller


class SellerController:
    @staticmethod
    def create_seller():
        body = request.get_json()
        result, status_code = SellerService.create_seller(body)
        return jsonify(result), status_code

    @staticmethod
    def activate_seller():
        body = request.get_json()
        result = SellerService.activate_seller(body)

        # Verifica se o resultado é uma tupla (erro) ou um dicionário (sucesso)
        if isinstance(result, tuple):
            message, status_code = result  # Desempacota a tupla
            return jsonify(message), status_code
        else:
            # Se for um dicionário (sucesso), retorna a mensagem e o código 200
            return jsonify(result), 200

    @staticmethod
    def login(email, password):
    # Verifique as credenciais do usuário
        user = Seller.query.filter_by(email=email).first()
        if user and user.password == password:  # trocar depois para hashing (senhas)
        # Use o ID do usuário como identity e adicione claims extras, se necessário
            access_token = create_access_token(
                identity=user.id,  
                additional_claims={"name": user.name, "status": user.status},
        )
            return jsonify(access_token=access_token), 200

        return jsonify({"mensagem": "Credenciais inválidas"}), 401


