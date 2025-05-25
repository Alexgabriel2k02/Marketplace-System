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
        user = Seller.query.filter_by(email=email).first()
        if not user or user.password != password:
            return jsonify({"mensagem": "Credenciais inválidas"}), 401

        if not user.name or not user.status:
            return jsonify({"mensagem": "Dados do vendedor incompletos. Contate o suporte."}), 400

        access_token = create_access_token(
            identity=user.id,
            additional_claims={"name": user.name, "status": user.status},
        )
        user_dict = user.to_dict()
        user_dict.pop("password", None)
        user_dict.pop("verification_code", None)
        return jsonify(token=access_token, user=user_dict), 200

    @staticmethod
    def list_sellers():
        result, status_code = SellerService.list_sellers()
        return jsonify(result), status_code


