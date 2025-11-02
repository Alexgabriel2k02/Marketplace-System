from flask import request, jsonify, current_app
from src.config.data_base import db
from src.Infrastructure.Model.payments import Payment
from src.Infrastructure.Model.sales import Sale
from src.Infrastructure.Model.product import Product


class PaymentsController:
    @staticmethod
    def webhook():
        # Recebe eventos assinados do gateway (simulação)
        signature = request.headers.get("X-Webhook-Signature") or request.headers.get("X-Signature")
        secret = current_app.config.get("WEBHOOK_SECRET", "defaultsecret")
        if signature != secret:
            return jsonify({"error": "invalid_signature"}), 403

        data = request.get_json() or {}
        event = data.get("event")
        gateway_id = data.get("gateway_id")
        order_id = data.get("order_id")
        status = data.get("status")

        payment = None
        if gateway_id:
            payment = Payment.query.filter_by(gateway_id=gateway_id).first()
        if not payment and order_id:
            try:
                payment = Payment.query.get(int(order_id))
            except Exception:
                payment = None

        if not payment:
            return jsonify({"error": "not_found", "message": "Payment not found"}), 404

        # Normalizar eventos/statuses simples
        lowered = (event or "").lower() + " " + (str(status) or "").lower()

        if "succeed" in lowered or "paid" in lowered or "success" in lowered:
            payment.status = "success"
            db.session.commit()
            return jsonify({"message": "Payment updated to success"}), 200

        if "fail" in lowered or "declin" in lowered or "rejected" in lowered:
            payment.status = "failed"
            # Reverter estoque para vendas associadas
            sales = Sale.query.filter_by(order_id=payment.id).all()
            for s in sales:
                product = Product.query.get(s.product_id)
                if product:
                    product.quantity = (product.quantity or 0) + (s.quantity or 0)
                    if product.quantity > 0:
                        product.status = "Ativo"
            db.session.commit()
            return jsonify({"message": "Payment failed, stock reverted"}), 200

        # Evento genérico: apenas armazenar
        payload = payment.payload or {}
        payload["last_event"] = data
        payment.payload = payload
        db.session.commit()
        return jsonify({"message": "Event received"}), 200
