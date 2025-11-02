from src.Infrastructure.Model.sales import Sale
from src.Infrastructure.Model.product import Product
from src.Infrastructure.Model.seller import Seller
from src.Infrastructure.Model.payments import Payment
from src.Infrastructure.Model.idempotency import IdempotencyKey
from src.config.data_base import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
import uuid
import base64


class SaleService:
    @staticmethod
    def create_sale(data, seller_id):
        """
        Espera o payload com 'items' (lista), 'total', 'payment_method', 'payment_details', 'customer', 'idempotency_key'.
        - Recalcula preços a partir do DB
        - Verifica estoque
        - Reserva estoque dentro de transação
        - Cria registros Sale por item
        - Cria registro Payment (simulado)
        - Suporta idempotency_key simples (persistido)
        """

        # Valida payload básico
        items = data.get("items")
        payment_method = data.get("payment_method")
        payment_details = data.get("payment_details", {})
        client = data.get("customer")
        idempotency_key = data.get("idempotency_key")

        if not items or not isinstance(items, list) or len(items) == 0:
            return {"error": "invalid_payload", "message": "Lista de items vazia ou inválida"}, 400

        # Idempotency: se fornecido, retorna a resposta anterior registrada
        if idempotency_key:
            existing = IdempotencyKey.query.filter_by(key=idempotency_key).first()
            if existing:
                # retornar resposta guardada (json armazenado em existing.response)
                try:
                    return existing.response_json, 200
                except Exception:
                    pass

        # Buscar e bloquear produtos para evitar condições de corrida
        product_ids = [int(item.get("product_id")) for item in items]
        products = Product.query.filter(Product.id.in_(product_ids)).with_for_update().all()
        products_map = {p.id: p for p in products}

        recalculated_total = 0.0
        insufficient = []

        # Valida cada item
        for item in items:
            pid = item.get("product_id")
            qty = item.get("quantity")
            if not pid or not isinstance(pid, int):
                return {"error": "invalid_item", "message": f"product_id inválido: {pid}"}, 400
            if not qty or not isinstance(qty, int) or qty <= 0:
                return {"error": "invalid_item", "message": f"quantity inválida para product {pid}"}, 400
            product = products_map.get(pid)
            if not product or product.status != "Ativo":
                return {"error": "not_found", "message": f"Produto {pid} não encontrado ou inativo"}, 404
            if product.quantity < qty:
                insufficient.append({"product_id": pid, "available": product.quantity, "requested": qty})
            recalculated_total += float(product.price) * qty

        if insufficient:
            return {"error": "out_of_stock", "message": "Estoque insuficiente", "details": insufficient}, 409

        # A partir daqui, todos os itens possuem estoque suficiente
        try:
            # Usar transação para criar pagamento e reservar estoque e criar vendas (associando order_id)
            with db.session.begin():
                # Criar registro de pagamento (simulado) em estado de processamento
                payment = Payment(
                    method=payment_method,
                    status="processing",
                    gateway_id=None,
                    amount=recalculated_total,
                    payload={"details": payment_details},
                )
                db.session.add(payment)
                # Garantir que payment.id seja gerado (flush) antes de criar as vendas para associar order_id
                db.session.flush()

                created_sales = []
                for item in items:
                    pid = item.get("product_id")
                    qty = item.get("quantity")
                    product = products_map[pid]

                    sale = Sale(
                        product_id=pid,
                        seller_id=seller_id,
                        order_id=payment.id,
                        quantity=qty,
                        unit_price=product.price,
                        total_price=product.price * qty,
                    )
                    db.session.add(sale)

                    # Reservar estoque (diminuição temporária)
                    product.quantity = product.quantity - qty
                    if product.quantity <= 0:
                        product.status = "Inativo"

                    created_sales.append(sale)

            # Simular chamada ao gateway (fora da transação DB principal)
            if payment_method == "credit":
                # Simular autorização imediata de sucesso
                payment.status = "success"
                payment.gateway_id = f"tx_{uuid.uuid4().hex[:12]}"
                db.session.commit()

                # Atualizar vendas criadas (não há order model robusto aqui) e retornar
                sale_ids = [s.id for s in created_sales]
                response = {
                    "order_id": payment.id,  # usar id do payment como agrupador simples
                    "status": "paid",
                    "payment": {
                        "method": "credit",
                        "gateway_id": payment.gateway_id,
                        "status": "success",
                    },
                    "sale_ids": sale_ids,
                    "message": "Pagamento aprovado",
                }
                # salvar idempotency
                if idempotency_key:
                    ik = IdempotencyKey(key=idempotency_key, response_json=response)
                    db.session.add(ik)
                    db.session.commit()

                return response, 201

            elif payment_method == "pix":
                # Gerar payload PIX simulado
                expiration = (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
                qrcode_text = f"000201PIX{uuid.uuid4().hex}"
                qr_b64 = base64.b64encode(qrcode_text.encode()).decode()

                payment.status = "waiting_payment"
                payment.gateway_id = f"pix_{uuid.uuid4().hex[:10]}"
                payment.payload = {"pix_payload": {"qr_code": qr_b64, "qrcode_text": qrcode_text, "expiration": expiration}}
                db.session.commit()

                sale_ids = [s.id for s in created_sales]
                response = {
                    "order_id": payment.id,
                    "status": "pending",
                    "payment": {
                        "method": "pix",
                        "status": "waiting_payment",
                        "pix_payload": payment.payload.get("pix_payload")
                    },
                    "sale_ids": sale_ids,
                    "message": "PIX gerado, aguarde confirmação",
                }
                if idempotency_key:
                    ik = IdempotencyKey(key=idempotency_key, response_json=response)
                    db.session.add(ik)
                    db.session.commit()
                return response, 201

            else:
                # Outros métodos (debit) - tratar como débito = captura imediata
                payment.status = "success"
                payment.gateway_id = f"tx_{uuid.uuid4().hex[:12]}"
                db.session.commit()
                sale_ids = [s.id for s in created_sales]
                response = {
                    "order_id": payment.id,
                    "status": "paid",
                    "payment": {"method": payment_method, "gateway_id": payment.gateway_id, "status": "success"},
                    "sale_ids": sale_ids,
                    "message": "Pagamento aprovado",
                }
                if idempotency_key:
                    ik = IdempotencyKey(key=idempotency_key, response_json=response)
                    db.session.add(ik)
                    db.session.commit()
                return response, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "server_error", "message": str(e)}, 500

    @staticmethod
    def list_sales():
        sales = Sale.query.order_by(Sale.created_at.desc()).all()
        sales_list = [sale.to_dict() for sale in sales]
        return sales_list, 200
